from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

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


@login_required()
def profile(request):
    user_update_form = UserUpdateForm(request.POST or None, instance=request.user)

    profile_update_form = ProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.profile,
    )

    if request.method == "POST":
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("user-profile")

    return render(
        request,
        "users/profile.html",
        {
            "title": "Profile",
            "profile": request.user.profile,
            "user_update_form": user_update_form,
            "profile_update_form": profile_update_form,
        },
    )
