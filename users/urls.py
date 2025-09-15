from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="user-register"),
    path("profile/", views.profile, name="user-profile"),
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
]
