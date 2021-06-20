from django.test import TestCase
from django.contrib.auth.models import User

from main_app.forms import BookmarkForm, TaskForm
from main_app.models import Tag

class BookmarkFormTest(TestCase):
    def test_labels(self):
        form = BookmarkForm()
        self.assertEqual(form.fields['title'].label, 'عنوان')
        self.assertEqual(form.fields['descr'].label, 'وصف')
        self.assertEqual(form.fields['url'].label, 'رابط')
        self.assertEqual(form.fields['tags'].label, 'وسوم')

    
    def test_only_user_tags(self):
        user1 = User.objects.create_user('foo', 'foo@email.com', '123456')
        user2 = User.objects.create_user('bar', 'bar@email.com', '123456')
        Tag.objects.create(name='tag1', user=user1)
        Tag.objects.create(name='tag2', user=user1)
        tag3 = Tag.objects.create(name='tag3', user=user2)
        form = BookmarkForm(data={'title': 'title', 'descr': 'descr', 'url': 'https://example.com'}, user=user2)
        form.full_clean()
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.fields['tags'].queryset), [tag3])

class TaskFormTest(TestCase):
    def test_labels(self):
        form = TaskForm()
        self.assertEqual(form.fields['name'].label, 'اسم')
        self.assertEqual(form.fields['descr'].label, 'وصف')
        self.assertEqual(form.fields['priority'].label, 'أولوية')
        self.assertEqual(form.fields['due_date'].label, 'تاريخ الاستحقاق')
        self.assertEqual(form.fields['due_time'].label, 'ساعة الاستحقاق')
        self.assertEqual(form.fields['tags'].label, 'وسوم')

    def test_only_user_tags(self):
        user1 = User.objects.create_user('foo', 'foo@email.com', '123456')
        user2 = User.objects.create_user('bar', 'bar@email.com', '123456')
        Tag.objects.create(name='tag1', user=user1)
        Tag.objects.create(name='tag2', user=user1)
        tag3 = Tag.objects.create(name='tag3', user=user2)
        form = TaskForm(data={'name': 'name', 'descr': 'descr', 'priority': 1, 'due_date': '3000-10-10', 'due_time': '05:30'}, user=user2)
        form.full_clean()
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.fields['tags'].queryset), [tag3])

    def test_min_priority(self):
        form = TaskForm(data={'name': 'name', 'descr': 'descr', 'priority': -22, 'due_date': '4000-05-04', 'due_time': '10:00'})
        self.assertFalse(form.is_valid())

    def test_due_date_in_past(self):
        form = TaskForm(data={'name': 'name', 'descr': 'descr', 'priority': 1, 'due_date': '2000-01-01', 'due_time': '00:00'})
        self.assertFalse(form.is_valid())
