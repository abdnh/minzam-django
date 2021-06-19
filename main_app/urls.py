from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.index, name='index'),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),

    path('bookmark/', views.BookmarkListView.as_view(), name='bookmarks'),
    path('bookmark/<int:pk>', views.BookmarkDetailView.as_view(), name='bookmark-detail'),
    path('bookmark/create/', views.create_bookmark, name='bookmark-create'),
    path('bookmark/<int:bookmark_id>/update/', views.update_bookmark, name='bookmark-update'),
    path('bookmark/<int:bookmark_id>/delete/', views.delete_bookmark, name='bookmark-delete'),

    path('task/', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', views.create_task, name='task-create'),
    path('task/<int:task_id>/update/', views.update_task, name='task-update'),
    path('task/<int:task_id>/delete/', views.delete_task, name='task-delete'),
    
    path('tag/', views.TagListView.as_view(), name='tags'),
    path('tag/<int:pk>', views.TagDetailView.as_view(), name='tag-detail'),
    path('tag/create/', views.create_tag, name='tag-create'),
    path('tag/<int:tag_id>/update/', views.update_tag, name='tag-update'),
    path('tag/<int:tag_id>/delete/', views.delete_tag, name='tag-delete'),
    
]
