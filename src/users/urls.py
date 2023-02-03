from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("profile/<int:pk>", views.UserProfileView.as_view(), name="profile"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("upload/", views.upload_file, name="upload_file")
]