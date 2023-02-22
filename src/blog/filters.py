import django_filters
from django.db.models import Q

from blog.models import Post

class PostFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(field_name='header', method='filter_q')

    def filter_q(self, queryset, name, value):
        return queryset.filter(
            Q(header__icontains = value) |
            Q(describe__icontains = value)
        )

    class Meta:
        model = Post
        fields = {
            'tags__name': ['in'],
            'categories__name': ['in'],
        }