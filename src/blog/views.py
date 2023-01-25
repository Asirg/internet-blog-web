from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import View
from django.contrib.auth import get_user_model

from blog.models import Post, Category

class IndexView(View):
    def get(self, request):
        context = {
            "last_update": Post.objects.all().order_by("-publication_date")[:5],
            "most_popular": Post.objects.all().order_by("-number_of_views")[:5],
            "news": Post.objects.filter(categories__in=[8]).order_by('-publication_date')[:5],
            "authors": get_user_model().objects.all()[:7],
        }
        return render(request, template_name="blog/index.html", context=context)

class PostByCategoryView(ListView):
    model = Post
    template_name = "blog/post_by_category.html"

    paginate_by = 10

    def get_queryset(self):
        category = Category.objects.get(url=self.kwargs.get("url")).get_sub_categories
        queryset = Post.objects\
                    .filter(categories__in = category)\
                    .order_by("-publication_date")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(url=self.kwargs.get("url"))
        context["popular_posts"] = Post.objects\
                                            .filter(categories__in = context["category"].get_sub_categories)\
                                            .order_by("-number_of_views")[:5]
        context["popular_tags"] = context["category"].get_popular_tags[:10]
        return context