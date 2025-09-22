from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from .models import Profile


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # You might want to log the user in and redirect to a different page
            messages.success(request, "Account created successfully!")
            return redirect("user-login")
        else:
            return render(
                request, "users/register.html", {"form": form, "title": "Register"}
            )

    else:  # GET request
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form, "title": "Register"})


user = get_user_model()


@login_required()
def profile(request, user_id=None):
    # If user_id is provided and the requester is a superuser, allow access to any user's profile.
    # Regular users can only access their own profile, even if they pass their own user_id.
    if user_id and request.user.is_superuser:

        user_obj = get_object_or_404(User, id=user_id)
    elif user_id and not request.user.is_superuser:
        messages.error(
            request, "You do not have permission to view other users' profiles."
        )
        return redirect("user-profile")
    else:
        user_obj = request.user

    user_update_form = UserUpdateForm(request.POST or None, instance=user_obj)
    profile_update_form = ProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=user_obj.profile,
    )

    if request.method == "POST":
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("user-profile", user_id=user_obj.id)
    # If AJAX → return only the form HTML for the modal
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "users/profile.html",
            {
                "user_update_form": user_update_form,
                "profile_update_form": profile_update_form,
            },
            request=request,
        )
        return JsonResponse({"html": html})
    return render(
        request,
        "users/profile.html",
        {
            "title": f"Profile of {user_obj.username}",
            "profile": user_obj.profile,
            "user_update_form": user_update_form,
            "profile_update_form": profile_update_form,
        },
    )
    # user_update_form = UserUpdateForm(request.POST or None, instance=request.user)

    # profile_update_form = ProfileUpdateForm(
    #     request.POST or None,
    #     request.FILES or None,
    #     instance=request.user.profile,
    # )

    # if request.method == "POST":
    #     if user_update_form.is_valid() and profile_update_form.is_valid():
    #         user_update_form.save()
    #         profile_update_form.save()
    #         messages.success(request, "Profile updated successfully!")
    #         return redirect("user-profile")

    # return render(
    #     request,
    #     "users/profile.html",
    #     {
    #         "title": "Profile",
    #         "profile": request.user.profile,
    #         "user_update_form": user_update_form,
    #         "profile_update_form": profile_update_form,
    #     },
    # )


@login_required()
def admin_access(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access ADMIN page.")
        return redirect("blog-home")

    return render(request, "users/admin.html", {"title": "Admin"})


def users_json(request):
    users = User.objects.annotate(total_posts=Count("posts"))
    data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "total_posts": user.total_posts,
        }
        for user in users
    ]
    return JsonResponse({"data": data})
