from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('category/<slug:category_slug>/', views.PostListView.as_view(), name='category_posts'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='tag_posts'),
    path('category/<slug:slug>/detail/', views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/detail/', views.tag_detail, name='tag_detail'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
