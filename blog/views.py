# from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Post

# Create your views here.
# def home(request):
#     """View function for home page of site."""

#     context = {"posts": Post.objects.all(), "title": "Home"}
#     return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 6

    def render_to_response(self, context, **response_kwargs):
        request = self.request
        page_obj = context["page_obj"]

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(request, "blog/post_partial.html", {"posts": page_obj})

        return super().render_to_response(context, **response_kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"  # <app>/<model>_<viewtype>.html


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "category", "content"]
    template_name = "blog/post_form.html"  # <app>/<model>_<viewtype>.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "category", "content"]
    # template_name = "blog/post_form.html"  # <app>/<model>_<viewtype>.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse_lazy(
            "user-posts", kwargs={"username": self.request.user.username}
        )

    # template_name = "blog/post_confirm_delete.html"  # <app>/<model>_<viewtype>.html

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/user_posts.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = User.objects.get(username=self.kwargs.get("username"))
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = "blog/category_posts.html"  # you can reuse home.html if you want
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs.get("category")).order_by(
            "-date_posted"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs.get("category")
        context["categories"] = (
            Post.objects.values_list("category", flat=True)
            .distinct()
            .exclude(category__isnull=True)
            .exclude(category__exact="")
        )

        return context


def about(request):
    """View function for about page of site."""

    return render(request, "blog/about.html", {"title": "About"})
