from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.base import View, TemplateView
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import JsonResponse

from blog.models import Post, Category, Tag, Reaction, Comment
from blog.forms import PostForm

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
        q = self.request.GET.get('q')
        tags = self.request.GET.getlist('tag')
        categories = self.request.GET.getlist('category')
        sort = self.request.GET.get('sort', '-number_of_views')

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
        context['args'] = {
            'q':self.request.GET.get('q', ''),
            'sort':self.request.GET.get('sort', '-number_of_views'),
            'category':self.request.GET.getlist('category'),
            'tag':self.request.GET.getlist('tag') ,
        }
        return context

############################## POST methods
class CreatePostView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    permission_required = ('blog.add_post', )

    def get_success_url(self) -> str:
        return reverse('blog:post_detail', kwargs={'pk':self.object.id})

class DeletePostView(PermissionRequiredMixin, DeleteView):
    model = Post

    permission_required = ('blog.delete_post', )

    def has_permission(self):
        user = self.request.user
        post = self.get_object()
        perms = self.get_permission_required()

        permission = user.has_perms(perms)
        author_post = post.author == user
        return  permission or author_post
    
    def get_success_url(self):
        return reverse('blog:index')
    

class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ('post', 'author', 'parent', 'content', )

    login_url = 'users:login'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk':self.request.POST.get('post')})

class DeleteCommentView(PermissionRequiredMixin, DeleteView):
    model = Comment

    permission_required = ('blog.delete_comment', )

    def has_permission(self):
        user = self.request.user
        comment = self.get_object()
        perms = self.get_permission_required()

        permission = user.has_perms(perms)
        author_comment = comment.author == user
        author_post = comment.post.author == user
        return  permission or author_comment or author_post 

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

class AddReactionPostView(LoginRequiredMixin, View):

    def post(self, request, pk):
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
        
        return JsonResponse({
            'likes': post.like_count,
            'dislikes': post.dislike_count,
        }, status=status)

class TagJsonView(View):
    def get(self, request):
        q = request.GET.get('q')
        queryset = Tag.objects.filter(name__contains=q).values("id", "name")[:6]
        return JsonResponse(list(queryset), safe=False)