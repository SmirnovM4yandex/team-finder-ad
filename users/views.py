from django.views import View
from django.views.generic import FormView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash

from .forms import RegisterForm, LoginForm, ProfileEditForm
from django.db.models import Q
from projects.models import Project
from .models import User
from django.contrib.auth.forms import PasswordChangeForm

class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()

        login(self.request, user)
        return redirect("users:login")
    
class UserLoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        login(self.request, user)

        return redirect("projects:project_list")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("projects:project_list")

class UsersListView(ListView):
    model = User
    template_name = "users/participants.html"
    context_object_name = "participants"
    paginate_by = 12

    def get_queryset(self):
        qs = User.objects.all().order_by("id")
        user = self.request.user

        filter_type = self.request.GET.get("filter")

        if not user.is_authenticated or not filter_type:
            return qs

        if filter_type == "owners-of-favorite-projects":
            return qs.filter(
                owned_projects__interested_users=user
            ).distinct()

        if filter_type == "owners-of-participating-projects":
            return qs.filter(
                owned_projects__participants=user
            ).distinct()

        if filter_type == "interested-in-my-projects":
            return qs.filter(
                favorites__owner=user
            ).distinct()

        if filter_type == "participants-of-my-projects":
            return qs.filter(
                participated_projects__owner=user
            ).distinct()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["active_filter"] = self.request.GET.get("filter", "")
        context["active_skill"] = None

        return context
    
class UserDetailView(DetailView):
    model = User
    template_name = "users/user-details.html"
    context_object_name = "user"
    pk_url_kwarg = "pk"

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = "users/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return f"/users/{self.request.user.pk}/"

class PasswordChangeView(LoginRequiredMixin, FormView):
    template_name = "users/change_password.html"
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return redirect("users:user_detail", pk=user.pk)