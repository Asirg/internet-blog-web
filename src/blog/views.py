from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.base import View, TemplateView

from blog.models import Post, Category, Tag, Reaction, Comment

class IndexView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_posts'] = Post.objects.all().order_by('-publication_date')[:5]
        context['popular_posts'] = Post.objects.all().order_by('-number_of_views')[:5]
        context['last_news_posts'] = Post.objects.filter(categories__in=[8]).order_by('-publication_date')[:5]
        return context

class PostDetailView(DetailView):
    model = Post
    
class PostByCategoryView(ListView):
    model = Post
    paginate_by = 10

    template_name = 'blog/post_by_category.html'

    def get_queryset(self):
        categories = Category.objects.get(url=self.kwargs.get('url')).get_sub_categories
        print(Category.objects.get(url=self.kwargs.get('url')))
        queryset = Post.objects\
                    .filter(categories__in=categories)\
                    .order_by('-publication_date').distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(url=self.kwargs.get('url'))
        context['popular_posts'] = Post.objects\
                                            .filter(categories__in=context['category'].get_sub_categories)\
                                            .order_by('-number_of_views').distinct()[:5]
        context['popular_tags'] = context['category'].get_popular_tags[:10]
        return context

class SearchView(ListView):
    model = Post
    paginate_by = 10

    template_name = 'blog/search.html'

    def get_queryset(self):
        queryset = Post.objects.all().order_by(sort)

        q = self.request.GET.get('q')
        tags = self.request.GET.getlist('tags')
        categories = self.request.GET.getlist('category')
        sort = self.request.GET.get('sort', '-number_of_views')

        if q:
            queryset = queryset.filter(header__icontains=q)
        if tags:
            queryset = queryset.filter(tags__name__in=tags)
        if categories:
            queryset = queryset.filter(categories__name__in = categories)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['sort'] = self.request.GET.get('sort', '-number_of_views')
        context['category_list'] = self.request.GET.getlist('category')
        context['tag_list'] = self.request.GET.getlist('tags') 
        return context

############################## POST methods
class CommentView(CreateView):
    model = Comment
    fields = ('post', 'author', 'parent', 'content', )

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk':self.request.POST.get('post')})

class DeleteCommentView(DeleteView):
    model = Comment
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk':self.object.post.id})

############################## Json return for fetch
class UpdateCommentView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        Comment.objects.filter(pk=comment.pk).update(content=request.POST.get("content"))

        return JsonResponse(
            {},
            status=200
        )

class AddReactionPostView(View):
    def post(self, request, pk):
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=pk)
            Reaction.objects.update_or_create(
                author=request.user,
                post=post,
                comment=None,
                defaults={
                    "like":request.POST.get('like'),
                }
            )
            status = 201
        else:
            status = 401
        
        return JsonResponse({
            'likes': post.like_count,
            'dislikes': post.dislike_count,
        }, status=status)

class TagJsonView(View):
    def get(self, request):
        q = request.GET.get('q')
        queryset = Tag.objects.filter(name__contains=q).values("id", "name")[:6]
        return JsonResponse(list(queryset), safe=False)
