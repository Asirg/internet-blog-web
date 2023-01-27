from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.contrib.auth import get_user_model
from django.db.models import Q

from blog.models import Post, Category, Tag

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
                    .order_by("-publication_date").distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(url=self.kwargs.get("url"))
        context["popular_posts"] = Post.objects\
                                            .filter(categories__in = context["category"].get_sub_categories)\
                                            .order_by("-number_of_views").distinct()[:5]
        context["popular_tags"] = context["category"].get_popular_tags[:10]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

class SearchView(ListView):
    model = Post
    template_name = "blog/search.html"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        
        tags = self.request.GET.getlist('tags')
        categories = self.request.GET.getlist('category')

        sort = self.request.GET.get('sort')
        sort = sort if sort else "-publication_date"

        queryset = Post.objects.all().order_by(sort)
        
        if q:
            queryset = queryset.filter(header__icontains=q)
        if tags:
            queryset = queryset.filter(tags__name__in=tags)
        if categories:
            queryset = queryset.filter(categories__name__in = categories)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['par'] = {
            "q": self.request.GET.get("q") if self.request.GET.get("q") else "",
            "sort": self.request.GET.get('sort') if self.request.GET.get("sort") else "-publication_date",
            "category_list": self.request.GET.getlist('category'),
            "tag_list": self.request.GET.getlist('tags') ,
        }
        return context

class TagView(View):
    def get(self, request):
        print(request.GET)
        query = request.GET.get('q')
        if query:
            return JsonResponse(list(Tag.objects.filter(name__contains=request.GET.get('q')).values("id", "name")), safe=False)
        else:
            return JsonResponse([], safe=False)