from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),
]