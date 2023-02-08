from django import template

from core.settings import STATIC_URL

register = template.Library()

@register.simple_tag()
def user_avatar(profile):
    if profile.avatar:
        return profile.avatar.url
    else:
        return "/" + STATIC_URL + "image/anonymous.png"