from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('tags/', views.TagJsonView.as_view(), name='tags'),
    path('category/<slug:url>', views.PostByCategoryView.as_view(), name='category'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post_reaction/<int:pk>', views.AddReactionPostView.as_view(), name='post_reaction'),
    path('add_comment/', views.CommentView.as_view(), name="add_comment"),
    path('delete_comment/<int:pk>.', views.DeleteCommentView.as_view(), name="delete_comment"),
    path('update_comment/<int:pk>', views.UpdateCommentView.as_view(), name="update_comment"),
]