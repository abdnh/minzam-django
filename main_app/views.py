from datetime import datetime
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Bookmark, Task, Tag
from .forms import BookmarkForm, TaskForm, TagForm, UserRegistrationForm


def index(request):
    return render(request, 'index.html')


class BookmarkListView(LoginRequiredMixin, generic.ListView):
    model = Bookmark
    paginate_by = 10

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).order_by('title')


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-due_date', 'priority')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        context['now'] = timezone.now()
        return super().get_context_data(**context)


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 10

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by('name')


class BookmarkDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Bookmark

    def test_func(self):
        return self.request.user == self.get_object().user


class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Task

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        context['now'] = timezone.now()
        return super().get_context_data(**context)


class TagDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Tag

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmarks'] = Bookmark.objects.filter(user=self.request.user, tags__name=self.object.name)
        context['tasks'] = Task.objects.filter(user=self.request.user, tags__name=self.object.name)
        return context


@login_required
def create_bookmark(request):

    if request.method == 'POST':
        form = BookmarkForm(data=request.POST)
        if form.is_valid():
            bookmark = Bookmark.objects.get_or_create(
                                            url=form.cleaned_data['url'],
                                            user=request.user)[0]
            bookmark.title = form.cleaned_data['title']
            bookmark.descr = form.cleaned_data['descr']
            bookmark.tags.set(form.cleaned_data['tags'])
            bookmark.save()
            return HttpResponseRedirect(reverse('bookmark-detail', kwargs={'pk': bookmark.id}))

    else:
        form = BookmarkForm(user=request.user)

    context = {
        'form': form,
    }

    return render(request, 'bookmark_form.html', context=context)


class BookmarkData(dict):
    def getlist(self, name):
        if name == 'tags':
            return map(lambda t: t[0], self.bookmark.tags.through.objects.filter(bookmark_id=self.bookmark.id).values_list('tag_id'))


@login_required
def update_bookmark(request, bookmark_id):

    bookmark = get_object_or_404(Bookmark, pk=bookmark_id, user=request.user)

    if request.method == 'POST':
        form = BookmarkForm(data=request.POST)
        if form.is_valid():
            bookmark.title = form.cleaned_data['title']
            bookmark.descr = form.cleaned_data['descr']
            bookmark.url = form.cleaned_data['url']
            bookmark.tags.set(form.cleaned_data['tags'])
            bookmark.save()
            return HttpResponseRedirect(reverse('bookmark-detail', kwargs={'pk': bookmark.id}))

    else:
        data = BookmarkData({
            'title': bookmark.title,
            'descr': bookmark.descr,
            'url': bookmark.url,
        })
        data.bookmark = bookmark
        form = BookmarkForm(user=request.user, data=data)

    context = {
        'form': form,
    }

    return render(request, 'bookmark_form.html', context=context)


@login_required
def delete_bookmark(request, bookmark_id):

    bookmark = get_object_or_404(Bookmark, pk=bookmark_id, user=request.user)

    if request.method == 'POST':
        bookmark.delete()
        return HttpResponseRedirect(reverse('bookmarks'))

    context = {
        'bookmark': bookmark,
    }

    return render(request, 'bookmark_confirm_delete.html', context=context)


@login_required
def create_task(request):

    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = Task.objects.create(name=form.cleaned_data['name'],
                                              descr=form.cleaned_data['descr'],
                                              priority=form.cleaned_data['priority'],
                                              due_date=timezone.make_aware(datetime.combine(form.cleaned_data['due_date'], form.cleaned_data['due_time'])),
                                              user=request.user)
            task.tags.set(form.cleaned_data['tags'])
            task.save()
            return HttpResponseRedirect(reverse('task-detail', kwargs={'pk': task.id}))

    else:
        form = TaskForm(user=request.user)

    context = {
        'form': form,
    }

    return render(request, 'task_form.html', context=context)


class TaskData(dict):
    def getlist(self, name):
        if name == 'tags':
            return map(lambda t: t[0], self.task.tags.through.objects.filter(task_id=self.task.id).values_list('tag_id'))


@login_required
def update_task(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.name = form.cleaned_data['name']
            task.descr = form.cleaned_data['descr']
            task.priority = form.cleaned_data['priority']
            new_due_date = timezone.make_aware(datetime.combine(form.cleaned_data['due_date'], form.cleaned_data['due_time']))
            # FIXME: resending emails for the same tasks doesn't seem to work sometimes even though notified is updated - race condition?
            task.notifed = new_due_date <= task.due_date
            task.due_date = new_due_date
            task.tags.set(form.cleaned_data['tags'])
            task.save()
            return HttpResponseRedirect(reverse('task-detail', kwargs={'pk': task.id}))
    else:
        naive_date = timezone.make_naive(task.due_date)
        data = TaskData({
            'name': task.name,
            'descr': task.descr,
            'priority': task.priority,
            'due_date': naive_date.date(),
            'due_time': naive_date.time(),
        })
        data.task = task
        form = TaskForm(user=request.user, data=data)

    context = {
        'form': form,
    }

    return render(request, 'task_form.html', context=context)


@login_required
def delete_task(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect(reverse('tasks'))

    context = {
        'task': task,
    }

    return render(request, 'task_confirm_delete.html', context=context)


@login_required
def create_tag(request):

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = Tag.objects.get_or_create(name=form.cleaned_data['name'], user=request.user)[0]
            return HttpResponseRedirect(reverse('tag-detail', kwargs={'pk': tag.id}))

    else:
        form = TagForm()

    context = {
        'form': form,
    }

    return render(request, 'tag_form.html', context=context)


@login_required
def update_tag(request, tag_id):

    tag = get_object_or_404(Tag, pk=tag_id, user=request.user)

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag.name = form.cleaned_data['name']
            tag.save()
            return HttpResponseRedirect(reverse('tag-detail', kwargs={'pk': tag.id}))

    else:
        data = {'name': tag.name}
        form = TagForm(data)

    context = {
        'form': form,
    }

    return render(request, 'tag_form.html', context=context)


@login_required
def delete_tag(request, tag_id):

    tag = get_object_or_404(Tag, pk=tag_id, user=request.user)

    if request.method == 'POST':
        tag.delete()
        return HttpResponseRedirect(reverse('tags'))

    context = {
        'tag': tag,
    }

    return render(request, 'tag_confirm_delete.html', context=context)


class SignUpView(generic.CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
