from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="profile_pics", default="profile_pics/default.jpg"
    )

    def __str__(self):
        return f"{self.user.username} Profile"
