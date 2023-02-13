from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.base import View, TemplateView
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import QuerySet
from typing import Any, Dict

from blog.models import Post, Tag, Reaction, Comment
from blog.forms import PostForm
from blog.service import category_by_kwargs
from blog.filters import PostFilter

class IndexView(TemplateView):
    """
    """
    template_name = 'blog/index.html'

class PostDetailView(DetailView):
    model = Post

class PostByCategoryView(ListView): # Переправить наиспользование тегов
    model = Post
    paginate_by = 1

    template_name = 'blog/post_by_category.html'
    
    def get_queryset(self) -> QuerySet[Post]:
        categories = category_by_kwargs(self.kwargs).get_sub_categories
        queryset = Post.objects\
                    .filter(categories__in=categories)\
                    .order_by('-publication_date').distinct()
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = category_by_kwargs(self.kwargs)
        return context

class SearchView(ListView): # Переправить на гет параметры - фронт
    model = Post
    paginate_by = 10

    template_name = 'blog/search.html'

    def get_queryset(self):
        sort = self.request.GET.get('sort', '-number_of_views')
        queryset = PostFilter(
            self.request.GET,
            queryset=Post.objects.all().order_by(sort)
        ).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['args'] = self.request.GET
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