from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import get_user_model

from blog.models import Post

class IndexView(View):
    def get(self, request):
        context = {
            "last_update": Post.objects.all().order_by("-publication_date")[:5],
            "most_popular": Post.objects.all().order_by("-number_of_views")[:5],
            "news": Post.objects.filter(categories__in=[8]).order_by('-publication_date')[:5],
            "authors": get_user_model().objects.all()[:7],
        }
        return render(request, template_name="blog/index.html", context=context)