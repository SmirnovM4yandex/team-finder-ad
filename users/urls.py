from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),

    path("list/", views.UsersListView.as_view(), name="user_list"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),

    path(
        "edit-profile/",
        views.ProfileEditView.as_view(),
        name="profile_edit",
    ),
    path(
        "change-password/",
        views.PasswordChangeView.as_view(),
        name="change_password",
    ),
]
