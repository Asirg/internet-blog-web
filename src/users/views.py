from django.views.generic.base import TemplateView
from django.views.generic import DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, Q, Avg, Sum, When, Case

from users.models import Profile
from blog.models import Category

class UserRegistrationView(CreateView):
    model = User
    fields = ('username', 'first_name', 'email', 'password', )
    template_name = 'users/registration.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.data['password'])
        self.object.save()
        
        Profile(user=self.object).save()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.object.user

        context['statictics_all'] = {
            **user.comments.all().aggregate(comments_count=Count('id')),
            **user.posts.all().aggregate(
                post_count=Count('id'),
                number_of_vies_sum=Sum('number_of_views')
            ),
            **user.posts.all().aggregate(
                likes = Count('id', filter=Q(reactions__like=True)),
                dislike = Count('id', filter=Q(reactions__like=False)),
            ),
        }
        context['statistics_by_category'] = Category.objects.all().annotate(
                count = Count('post_category__id', filter=Q(post_category__author=user)),
                likes = Count('post_category__reactions__id', filter=Q(post_category__reactions__like=True) & Q(post_category__author=user)),
                dislikes = Count('post_category__reactions__id', filter=Q(post_category__reactions__like=False) & Q(post_category__author=user)),
                number_of_views_sum = Sum('post_category__number_of_views', filter=Q(post_category__author=user))
        ).filter(count__gt=0).values('name', 'count', 'likes', 'dislikes')
        return context

class DeleteUserView(PermissionRequiredMixin, DeleteView):
    model = User

    permission_required = 'users.delete_profile'

    def has_permission(self):
        permission = super().has_permission()
        is_owner =  self.request.user.id == self.kwargs['pk']
        return is_owner or permission
    def get_success_url(self):
        return reverse('blog:index')

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