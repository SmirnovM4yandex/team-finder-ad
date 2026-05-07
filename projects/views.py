from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from .models import Project
from .forms import ProjectForm

User = settings.AUTH_USER_MODEL

class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        return Project.objects.select_related("owner").order_by("-created_at")
    
class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project-details.html"
    context_object_name = "project"

class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        user = request.user

        if user.favorites.filter(pk=project.pk).exists():
            user.favorites.remove(project)
            favorited = False
        else:
            user.favorites.add(project)
            favorited = True

        return JsonResponse({
            "status": "ok",
            "favorited": favorited
        })
    
class ToggleParticipateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        user = request.user

        if user in project.participants.all():
            project.participants.remove(user)
            participating = False
        else:
            project.participants.add(user)
            participating = True

        return JsonResponse({
            "status": "ok",
            "participating": participating
        })

class FavoriteProjectsView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/favorite_projects.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        return self.request.user.favorites.select_related("owner").order_by("-created_at")
    
class CompleteProjectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        if project.owner != request.user:
            return JsonResponse({"status": "error"}, status=403)

        if project.status != "open":
            return JsonResponse({"status": "error"}, status=400)

        project.status = "closed"
        project.save()

        return JsonResponse({
            "status": "ok",
            "project_status": "closed"
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

        return redirect(f"/projects/{project.id}/")
    
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            return redirect("/projects/list/")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return f"/projects/{self.object.id}/"