from django import template
from blog.models import Category

register = template.Library()

@register.simple_tag()
def get_main_categories():
    return Category.objects.filter(parent__isnull=True)