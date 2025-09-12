from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # You might want to log the user in and redirect to a different page
            messages.success(request, "Account created successfully!")
            return redirect("blog-home")
        else:
            return render(request, "users/register.html", {"form": form})

    else:  # GET request
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})
