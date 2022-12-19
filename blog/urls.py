from django.urls import path
from . import views



urlpatterns = [
    path('', views.PostListView.as_view(), name="home"),
    path('users/<str:username>/', views.user_posts, name="user-page"),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('about/', views.about, name="about"),
    path('posts/new', views.CreatePost.as_view(), name="new-post"),
    path('posts/<int:pk>/edit', views.UpdatePost.as_view(), name='update-post'),
    path('posts/<int:pk>/delete', views.DeletePost.as_view(), name='post-delete'),
]