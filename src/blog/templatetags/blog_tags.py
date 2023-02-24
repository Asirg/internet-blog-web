from django.db.models import QuerySet
from django import template
from typing import Dict, Union

from blog.models import Category, Post, Tag


register = template.Library()

@register.simple_tag()
def link_page_with_args(page: int, args: dict) -> str:
    link = f"?page={page}&"
    print(link)
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

def filter_by_category(queryset, category):
    if category:
        try:
            category = Category.objects.get(name=category)
            queryset = queryset.filter(categories__in=category.get_sub_categories).distinct()
        except Category.objects.model.DoesNotExist:
            return []
    return queryset

@register.simple_tag()
def get_last_posts(category: str = "", count: int = 5) -> QuerySet[Post]:
    queryset = Post.objects.all().order_by('-publication_date')
    queryset = filter_by_category(queryset, category)
    return queryset[:count]

@register.simple_tag()
def get_popular_posts(category: str = '', count: int = 5) -> QuerySet[Post]:
    queryset = Post.objects.all().order_by('-number_of_views')
    queryset = filter_by_category(queryset, category)
    return queryset[:count]
    

@register.simple_tag()
def get_popular_tags(category: str = '', count: int =10) -> QuerySet[Tag]:
    return category.get_popular_tags[:count]