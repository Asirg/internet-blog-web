import django_filters

from blog.models import Post

class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
            'tags__name': ['in'],
            'categories__name': ['in'],
        }