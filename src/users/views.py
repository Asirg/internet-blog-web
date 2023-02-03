from django.views.generic.base import TemplateView
from django.views.generic import DetailView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from users.forms import UlpoadFileForm
from users.models import Profile

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
    model = User
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UlpoadFileForm()
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

    return redirect(reverse("users:profile", kwargs={'pk':request.user.id}))