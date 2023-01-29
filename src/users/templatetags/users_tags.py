from django import template

from core.settings import STATIC_URL

register = template.Library()

@register.simple_tag()
def user_avatar(user):
    if user.profile.avatar:
        return user.profile.avatar.url
    else:
        return "/" + STATIC_URL + "image/anonymous.png"