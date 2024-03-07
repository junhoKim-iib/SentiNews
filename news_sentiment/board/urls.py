from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostDeleteView,
    PostEditView,
    CommentCreateView,
    CommentDeleteView,
    CommentEditView,
)

app_name = 'board'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/edit/', CommentEditView.as_view(), name='comment_edit'),
]