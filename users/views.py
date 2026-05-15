from django.contrib.auth import (
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from core.constants import (
    DEFAULT_PAGE_SIZE,
    USER_FILTER_INTERESTED_IN_MY_PROJECTS,
    USER_FILTER_OWNERS_OF_FAVORITES,
    USER_FILTER_OWNERS_OF_PARTICIPATING,
    USER_FILTER_PARTICIPANTS_OF_MY_PROJECTS,
)

from users.forms import (
    LoginForm,
    ProfileEditForm,
    RegisterForm,
)
from users.models import User


class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)

        user.set_password(
            form.cleaned_data["password"]
        )

        user.save()

        login(self.request, user)

        return redirect("projects:project_list")


class UserLoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = form.cleaned_data["user"]

        login(self.request, user)

        return redirect("projects:project_list")


class UserLogoutView(View):
    def get(self, request):
        logout(request)

        return redirect("projects:project_list")


class UsersListView(ListView):
    model = User
    template_name = "users/participants.html"
    context_object_name = "participants"
    paginate_by = DEFAULT_PAGE_SIZE

    def get_queryset(self):
        queryset = User.objects.order_by("id")

        user = self.request.user

        filter_type = self.request.GET.get("filter")

        if not user.is_authenticated or not filter_type:
            return queryset

        filters = {
            USER_FILTER_OWNERS_OF_FAVORITES: {
                "owned_projects__interested_users": user,
            },
            USER_FILTER_OWNERS_OF_PARTICIPATING: {
                "owned_projects__participants": user,
            },
            USER_FILTER_INTERESTED_IN_MY_PROJECTS: {
                "favorites__owner": user,
            },
            USER_FILTER_PARTICIPANTS_OF_MY_PROJECTS: {
                "participated_projects__owner": user,
            },
        }

        if filter_type in filters:
            return queryset.filter(
                **filters[filter_type]
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["active_filter"] = (
            self.request.GET.get("filter", "")
        )

        return context


class UserDetailView(DetailView):
    model = User
    template_name = "users/user-details.html"
    context_object_name = "user"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = "users/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            "users:user_detail",
            kwargs={
                "pk": self.request.user.pk,
            },
        )


class PasswordChangeView(
    LoginRequiredMixin,
    FormView,
):
    template_name = "users/change_password.html"
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["user"] = self.request.user

        return kwargs

    def form_valid(self, form):
        user = form.save()

        update_session_auth_hash(
            self.request,
            user,
        )

        return redirect(
            "users:user_detail",
            pk=user.pk,
        )
