from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('tags/', views.TagView.as_view(), name='tags'),
    path('category/<slug:url>', views.PostByCategoryView.as_view(), name='category'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post_reaction/<int:pk>', views.AddReactionPostView.as_view(), name='post_reaction')
]