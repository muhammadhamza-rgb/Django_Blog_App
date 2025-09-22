from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import SendGridPasswordResetForm

urlpatterns = [
    path("post/json/", views.users_json, name="blog-home-json"),
    path("register/", views.register, name="user-register"),
    path("profile/", views.profile, name="user-profile"),
    # admin (or someone with permissions) can edit other user’s profile
    path("profile/<int:user_id>/", views.profile, name="user-profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html", extra_context={"title": "Login"}
        ),
        name="user-login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="users/logout.html", extra_context={"title": "Logout"}
        ),
        name="user-logout",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            form_class=SendGridPasswordResetForm,
            extra_context={"title": "Password Reset"},
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
            extra_context={"title": "Password Reset Done"},
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            extra_context={"title": "Password Reset Confirm"},
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
            extra_context={"title": "Password Reset Complete"},
        ),
        name="password_reset_complete",
    ),
    path("admin/", views.admin_access, name="admin"),
]
