from django.urls import path

from blog import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("category/<slug:url>", views.PostByCategoryView.as_view(), name="category"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="post_detail")
]