from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from users.forms import UserRegistrationForm
from users.models import UserProfile

class RegistrationView(View):
    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, 'users/registration.html', context={"user_form":user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.data['password'])
            new_user.save()
            UserProfile(
                user=new_user,
                avatar=None,
                bio="",
            ).save()
            
            login(request, new_user)

            return redirect(reverse("users:profile"))

        return redirect(reverse('users:registration'))

class UserLoginView(View):
    def get(self, request):
        return render(request, "users/login.html", context={})
    
    def post(self, request):
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user:
            login(request, user)
            return redirect(reverse('blog:index'))
        else:
            return redirect(reverse('users:login'))

def user_logout(request):
    logout(request)
    return redirect(reverse('blog:index'))

class UserProfileView(View):
    def get(self, request):
        return render(request, "users/profile.html", context={})