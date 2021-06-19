from django.contrib import admin

from .models import Bookmark, Task, Tag

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'user')
    search_fields = ['title', 'url']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'descr', 'user')
    list_filter = ['name']
    search_fields = ['name', 'descr']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
