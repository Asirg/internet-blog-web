from django.db.models import Q, Sum, Count

from users.models import Profile
from blog.models import Category


def get_context_for_profile(user):
    context = {}
    context['statistics_all'] = {
        **user.comments.all().aggregate(comments_count=Count('id')),
        **user.posts.all().aggregate(
            posts_count=Count('id'),
            number_of_views_sum=Sum('number_of_views')
        ),
        **user.posts.all().aggregate(
            likes = Count('id', filter=Q(reactions__like=True)),
            dislikes = Count('id', filter=Q(reactions__like=False)),
        ),
    }
    context['statistics_by_category'] = Category.objects.all().annotate(
        count = Count('post_category__id', filter=Q(post_category__author=user), distinct=True),
        likes = Count('post_category__reactions__id', filter=Q(post_category__reactions__like=True) & Q(post_category__author=user)),
        dislikes = Count('post_category__reactions__id', filter=Q(post_category__reactions__like=False) & Q(post_category__author=user)),
        number_of_views_sum = Sum('post_category__number_of_views', filter=Q(post_category__author=user))
    ).filter(count__gt=0).values('name', 'count', 'likes', 'dislikes')
    context['most_popular_posts'] = user.posts.all().order_by('-number_of_views')[:3]
    context['last_comments'] = user.comments.all().order_by('-date')[:5]
    return context