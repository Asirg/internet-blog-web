from django.db.models import QuerySet
from django import template

from blog.models import Post


register = template.Library()

@register.inclusion_tag('blog/elements/index_content_block.html')
def index_posts_block(header:str, posts: QuerySet[Post]):
    return {
        'header':header,
        'posts': posts
    }
