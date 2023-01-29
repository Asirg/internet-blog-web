from django.contrib import admin

from users.models import Profile



@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", )