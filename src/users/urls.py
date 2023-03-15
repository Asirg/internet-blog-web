from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/posts/<int:pk>', views.UserProfilePostsView.as_view(), name='posts'),
    path('profile/comments/<int:pk>/', views.UserProfileCommentsView.as_view(), name='comments'),

    path('delete_user/<int:pk>', views.DeleteUserView.as_view(), name="delete_user"),

    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload_file, name='upload_file'),
]