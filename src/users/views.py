from django.views.generic.base import TemplateView
from django.views.generic import DetailView, CreateView, DeleteView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from users.models import Profile
from blog.models import Post, Comment
from users import service

class UserRegistrationView(CreateView):
    model = User
    fields = ('username', 'first_name', 'email', 'password', )
    template_name = 'users/registration.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.data['password'])
        self.object.save()

        login(self.request, self.object)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("users:profile", kwargs={'pk':self.object.id})

class UserLoginView(TemplateView):
    template_name = "users/login.html"
    
    def post(self, request):
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            return redirect(reverse('blog:index'))
        return self.get(request)

class UserProfileView(DetailView):
    model = Profile
    template_name = 'users/profile.html'

class DeleteUserView(PermissionRequiredMixin, DeleteView):
    model = User

    permission_required = 'users.delete_profile'

    def has_permission(self):
        permission = super().has_permission()
        is_owner =  self.request.user.id == self.kwargs['pk']
        return is_owner or permission
    def get_success_url(self):
        return reverse('blog:index')

class UserProfilePostsView(ListView):
    model = Post
    template_name = 'users/user_posts.html'
    paginate_by = 10

    def get_queryset(self):
        user = Profile.objects.get(id=self.kwargs['pk']).user
        return Post.objects.filter(author=user).order_by('-number_of_views')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(id=self.kwargs['pk'])
        return context

class UserProfileCommentsView(ListView):
    model = Comment
    template_name = 'users/user_comments.html'
    paginate_by = 20

    def get_queryset(self):
        print(self)
        user = Profile.objects.get(id=self.kwargs['pk']).user
        return Comment.objects.filter(author=user).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(id=self.kwargs['pk'])
        return context

############################## functions
def user_logout(request):
    logout(request)
    return redirect(reverse('blog:index'))

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()

        filepath = f'user_avatar/{request.user.id}.'
        if fs.exists(filepath + 'png'):
            fs.delete(filepath + 'png')
        elif fs.exists(filepath + 'jpg'):
            fs.delete(filepath + 'jpg')
        
        filepath = fs.save(filepath + file.name.split(".")[-1], file)

        request.user.profile.avatar = filepath
        request.user.profile.save()

    return redirect(reverse("users:profile", kwargs={'pk':request.user.profile.id}))