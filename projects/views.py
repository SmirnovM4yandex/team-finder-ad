from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from core.constants import (
    DEFAULT_PAGE_SIZE,
    OWNER_CANNOT_LEAVE_MESSAGE,
    PROJECT_CLOSED_MESSAGE,
    PROJECT_STATUS_CLOSED,
    PROJECT_STATUS_OPEN,
    STATUS_ERROR,
    STATUS_OK,
)

from projects.forms import ProjectForm
from projects.models import Project


User = settings.AUTH_USER_MODEL


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = DEFAULT_PAGE_SIZE

    def get_queryset(self):
        return (
            Project.objects
            .select_related("owner")
            .prefetch_related("participants")
            .order_by("-created_at")
        )


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project-details.html"
    context_object_name = "project"

    def get_queryset(self):
        return (
            Project.objects
            .select_related("owner")
            .prefetch_related("participants")
        )


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = Project.objects.filter(
            pk=pk,
        ).first()

        if project is None:
            return JsonResponse(
                {
                    "status": STATUS_ERROR,
                    "message": "Project not found",
                },
                status=HTTPStatus.NOT_FOUND,
            )

        user = request.user

        is_favorited = user.favorites.filter(
            pk=project.pk,
        ).exists()

        if is_favorited:
            user.favorites.remove(project)
        else:
            user.favorites.add(project)

        return JsonResponse({
            "status": STATUS_OK,
            "favorited": not is_favorited,
        })


class ToggleParticipateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = Project.objects.filter(
            pk=pk,
        ).first()

        if project is None:
            return JsonResponse(
                {
                    "status": STATUS_ERROR,
                    "message": "Project not found",
                },
                status=HTTPStatus.NOT_FOUND,
            )
        user = request.user

        if project.owner == user:
            return JsonResponse(
                {
                    "status": STATUS_ERROR,
                    "message": OWNER_CANNOT_LEAVE_MESSAGE,
                },
                status=HTTPStatus.BAD_REQUEST,
            )

        if project.status == PROJECT_STATUS_CLOSED:
            return JsonResponse(
                {
                    "status": STATUS_ERROR,
                    "message": PROJECT_CLOSED_MESSAGE,
                },
                status=HTTPStatus.BAD_REQUEST,
            )

        is_participant = project.participants.filter(
            id=user.id,
        ).exists()

        if is_participant:
            project.participants.remove(user)
        else:
            project.participants.add(user)

        return JsonResponse({
            "status": STATUS_OK,
            "participant": not is_participant,
        })


class FavoriteProjectsView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/favorite_projects.html"
    context_object_name = "projects"
    paginate_by = DEFAULT_PAGE_SIZE

    def get_queryset(self):
        return (
            self.request.user.favorites
            .select_related("owner")
            .order_by("-created_at")
        )


class CompleteProjectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = Project.objects.filter(
            pk=pk,
        ).first()

        if project is None:
            return JsonResponse(
                {
                    "status": STATUS_ERROR,
                    "message": "Project not found",
                },
                status=HTTPStatus.NOT_FOUND,
            )

        if project.owner != request.user:
            return JsonResponse(
                {
                    "status": STATUS_ERROR
                },
                status=HTTPStatus.FORBIDDEN,
            )

        if project.status != PROJECT_STATUS_OPEN:
            return JsonResponse(
                {
                    "status": STATUS_ERROR
                },
                status=HTTPStatus.BAD_REQUEST,
            )

        project.status = PROJECT_STATUS_CLOSED
        project.save()

        return JsonResponse({
            "status": STATUS_OK,
            "project_status": PROJECT_STATUS_CLOSED,
        })


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"

    def form_valid(self, form):
        project = form.save(commit=False)

        project.owner = self.request.user

        project.save()

        project.participants.add(self.request.user)

        return redirect(
            "projects:project_detail",
            pk=project.pk,
        )


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"

    def get_queryset(self):
        return Project.objects.filter(
            owner=self.request.user
        )

    def get_success_url(self):
        return reverse(
            "projects:project_detail",
            kwargs={
                "pk": self.object.pk,
            },
        )
