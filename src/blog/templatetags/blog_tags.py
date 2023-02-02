from django import template

from blog.models import Category, Post


register = template.Library()

# @register.simple_tag()
# def get_popular_posts(count=5, *category):
#     queryset = Post.objects.all().order_by("-number_of_views")
#     if category:
#         queryset = queryset.filter(categories__in = category)
#     return queryset.distinct()[:count]

# @register.simple_tag()
# def get_last_posts(count=5, *category):
#     queryset = Post.objects.all().order_by("-number_of_views")
#     if category:
#         queryset = queryset.filter(categories__in = category)
#     return queryset.distinct()[:count]

@register.simple_tag()
def get_main_categories():
    return Category.objects.filter(parent__isnull=True)