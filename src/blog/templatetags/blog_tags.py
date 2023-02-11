from django.db.models import QuerySet
from django import template
from typing import Dict, Union

from blog.models import Category, Post, Tag


register = template.Library()

@register.simple_tag()
def link_page_with_args(page: int, args: dict) -> str:
    link = f"?page={page}&"
    if args:
        for key, value in args.items():
            if value != [] and value != '':
                if type(value) == list:
                    link += '&'.join([
                        f'{key}={val}' for val in value
                    ])
                else:
                    link += f"{key}={value}"
                link += "&"
    return link

@register.simple_tag()
def get_main_categories() -> QuerySet[Category]:
    return Category.objects.filter(parent__isnull=True)

@register.simple_tag()
def get_popular_posts(category: Category, count: int = 5) -> QuerySet[Post]:
    return Post.objects\
            .filter(categories__in=category.get_sub_categories)\
            .order_by('-number_of_views').distinct()[:count]

@register.simple_tag()
def get_popular_tags(category: Category, count: int =10) -> QuerySet[Tag]:
    return category.get_popular_tags[:count]