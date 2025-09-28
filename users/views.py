from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from .models import Profile

user = get_user_model()


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
        user_form = UserUpdateForm(request.POST, instance=user_obj)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user_obj.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return JsonResponse({"success": True})
        else:
            # log errors for debugging
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)

            # for AJAX, return rendered form with errors
            context = {
                "user_update_form": user_form,
                "profile_update_form": profile_form,
                "user": user_obj,
            }
            return render(
                request, "partials/profile_update_form.html", context, status=400
            )

    # GET → return form partial
    user_form = UserUpdateForm(instance=user_obj)
    profile_form = ProfileUpdateForm(instance=user_obj.profile)
    context = {
        "user_update_form": user_form,
        "profile_update_form": profile_form,
        "user": user_obj,
    }

    if user_id and request.user.is_superuser:
        return render(
            request,
            "partials/profile_update_form.html",
            {
                "title": f"{user_obj.username}'s Profile",
                "profile": user_obj.profile,
                "user_update_form": user_update_form,
                "profile_update_form": profile_update_form,
            },
        )

    if user_obj == request.user:
        return render(
            request,
            "users/profile.html",
            {
                "title": "Profile",
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


@login_required
def delete_profile(request, user_id=None):

    user_obj = User.objects.filter(id=user_id).first()

    if request.user.is_superuser:
        if user_obj.is_active:
            User.objects.filter(id=user_id).update(is_active=False)
            messages.info(request, "Profile has been deleted.")
            return JsonResponse(
                {"success": True, "status": "deleted", "redirect_url": "/users/admin/"}
            )

        messages.error(request, "Profile already deleted")
        return JsonResponse(
            {
                "success": True,
                "status": "already_deleted",
                "redirect_url": "/users/admin/",
            }
        )
    else:
        messages.error(
            request,
            "You don't have permission to delete a user, please contact admin at abc@xyz.com",
        )
        return JsonResponse(
            {
                "success": False,
                "status": "Permission_denied",
                "redirect_url": "/users/profile/",
            }
        )


@login_required()
def admin_access(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access ADMIN page.")
        return redirect("blog-home")

    return render(request, "users/admin.html", {"title": "Admin"})


def users_json(request):
    users = User.objects.filter(is_active=True).annotate(total_posts=Count("posts"))
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
