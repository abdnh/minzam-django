from django.utils import timezone
from django.test import TestCase

from main_app.models import Bookmark, Task, Tag

class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name='my tag')

    def test_name_label(self):
        tag = Tag.objects.get(id=1)
        name = tag._meta.get_field('name').verbose_name
        self.assertEqual(name, 'اسم')

    def test_name_max_length(self):
        tag = Tag.objects.get(id=1)
        maxlen = tag._meta.get_field('name').max_length
        self.assertEqual(maxlen, 255)

    def test_get_absolute_url(self):
        tag = Tag.objects.get(id=1)
        self.assertEqual(tag.get_absolute_url(), '/tag/1')


class BookmarkModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Bookmark.objects.create(title='my favorite site', descr='some description', url='https://example.com/')

    def test_title_label(self):
        bookmark = Bookmark.objects.get(id=1)
        title = bookmark._meta.get_field('title').verbose_name
        self.assertEqual(title, 'عنوان')

    def test_descr_label(self):
        bookmark = Bookmark.objects.get(id=1)
        descr = bookmark._meta.get_field('descr').verbose_name
        self.assertEqual(descr, 'وصف')

    def test_url_label(self):
        bookmark = Bookmark.objects.get(id=1)
        url = bookmark._meta.get_field('url').verbose_name
        self.assertEqual(url, 'رابط')

    def test_tags_label(self):
        bookmark = Bookmark.objects.get(id=1)
        url = bookmark._meta.get_field('tags').verbose_name
        self.assertEqual(url, 'وسوم')

    def test_title_max_length(self):
        bookmark = Bookmark.objects.get(id=1)
        maxlen = bookmark._meta.get_field('title').max_length
        self.assertEqual(maxlen, 255)

    def test_get_absolute_url(self):
        bookmark = Bookmark.objects.get(id=1)
        self.assertEqual(bookmark.get_absolute_url(), '/bookmark/1')


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Task.objects.create(name='an arduous task', descr='some description', priority=1, due_date=timezone.now())

    def test_name_label(self):
        task = Task.objects.get(id=1)
        name = task._meta.get_field('name').verbose_name
        self.assertEqual(name, 'اسم')

    def test_descr_label(self):
        task = Task.objects.get(id=1)
        descr = task._meta.get_field('descr').verbose_name
        self.assertEqual(descr, 'وصف')

    def test_priority_label(self):
        task = Task.objects.get(id=1)
        priority = task._meta.get_field('priority').verbose_name
        self.assertEqual(priority, 'أولوية')

    def test_tags_label(self):
        task = Task.objects.get(id=1)
        url = task._meta.get_field('tags').verbose_name
        self.assertEqual(url, 'وسوم')

    def test_name_max_length(self):
        task = Task.objects.get(id=1)
        maxlen = task._meta.get_field('name').max_length
        self.assertEqual(maxlen, 255)

    def test_get_absolute_url(self):
        task = Task.objects.get(id=1)
        self.assertEqual(task.get_absolute_url(), '/task/1')

