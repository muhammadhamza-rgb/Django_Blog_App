# from django.http import HttpResponse
from django.shortcuts import render

from .models import Post


# Create your views here.
def home(request):
    """View function for home page of site."""

    context = {"posts": Post.objects.all(), "title": "Home"}
    return render(request, "blog/home.html", context)


def about(request):
    """View function for about page of site."""

    return render(request, "blog/about.html", {"title": "About"})
