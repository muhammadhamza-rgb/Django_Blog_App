from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    # --- new field ---
    CATEGORY_CHOICES = [
        ("Technology", "Technology"),
        ("Health", "Health"),
        ("Education", "Education"),
        ("Travel", "Travel"),
        ("Food", "Food"),
        ("Lifestyle", "Lifestyle"),
        ("Finance", "Finance"),
        ("Others", "Others"),
    ]
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default="Others",
    )

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("post-detail", kwargs={"pk": self.pk})
