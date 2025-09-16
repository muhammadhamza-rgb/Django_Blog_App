from django.urls import path

from . import views

# from .views import PostCreateView, PostDetailView, PostListView

urlpatterns = [
    path("", views.PostListView.as_view(), name="blog-home"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("about/", views.about, name="blog-about"),
]
