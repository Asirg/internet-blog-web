from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="profile"
    )
    avatar = models.ImageField("avatar", upload_to="user_avatar/", null=True)
    bio = models.TextField("biografi")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"