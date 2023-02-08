from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name='profile'
    )
    avatar = models.ImageField('avatar', upload_to='user_avatar/', null=True, blank=True)
    bio = models.TextField('biografi', default='', blank=True)
    subscription = models.BooleanField('subscription', default=True)

    @property
    def most_popular_posts(self):
        return self.user.posts.all().order_by('-number_of_views')[:5]

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'