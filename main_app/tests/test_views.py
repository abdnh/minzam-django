import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from main_app.models import Bookmark, Task, Tag

class BookmarkListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('foo', 'foo@email.com', '123456')
        number_of_bookmarks = 13

        for bookmark_id in range(number_of_bookmarks):
            Bookmark.objects.create(
                title=f'bookmark {bookmark_id}',
                descr='',
                url='',
                user=cls.user
            )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/bookmark/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('bookmarks'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('bookmarks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/bookmark_list.html')

    def test_pagination_is_ten(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('bookmarks'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['bookmark_list']), 10)

    def test_lists_all_bookmarks(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('bookmarks')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['bookmark_list']), 3)

    def test_non_logged_in(self):
        response = self.client.get(reverse('bookmarks'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/bookmark/')


class TaskListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('foo', 'foo@email.com', '123456')
        number_of_tasks = 13

        for task_id in range(number_of_tasks):
            Task.objects.create(
                name=f'task {task_id}',
                descr='',
                due_date=timezone.now(),
                priority=1,
                user=cls.user
            )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/task/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/task_list.html')

    def test_pagination_is_ten(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['task_list']), 10)

    def test_lists_all_tasks(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['task_list']), 3)

    def test_non_logged_in(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/task/')


class TagListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('foo', 'foo@email.com', '123456')
        number_of_tags = 13

        for tag_id in range(number_of_tags):
            Tag.objects.create(
                name=f'tag {tag_id}',
                user=cls.user
            )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/tag/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tags'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tags'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/tag_list.html')

    def test_pagination_is_ten(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tags'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['tag_list']), 10)

    def test_lists_all_tags(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tags')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['tag_list']), 3)

    def test_non_logged_in(self):
        response = self.client.get(reverse('tags'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/tag/')


class BookmarkDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('foo', 'foo@email.com', '123456')
        cls.user2 = User.objects.create_user('bar', 'bar@email.com', '123456')
        Bookmark.objects.create(
            title='user1 bookmark',
            descr='',
            url='',
            user=cls.user1
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user1)
        response = self.client.get('/bookmark/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('bookmark-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user1)
        response = self.client.get('/bookmark/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/bookmark_detail.html')

    def test_non_logged_in_cannot_access_bookmarks(self):
        response = self.client.get('/bookmark/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/bookmark/1')

    def test_user_cannot_access_other_users_bookmarks(self):
        self.client.force_login(self.user2)
        response = self.client.get('/bookmark/1')
        self.assertEqual(response.status_code, 403)


class TaskDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('foo', 'foo@email.com', '123456')
        cls.user2 = User.objects.create_user('bar', 'bar@email.com', '123456')
        Task.objects.create(
            name='user1 task',
            descr='',
            priority=1,
            due_date=timezone.now(),
            user=cls.user1
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user1)
        response = self.client.get('/task/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('task-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user1)
        response = self.client.get('/task/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/task_detail.html')

    def test_non_logged_in_cannot_access_tasks(self):
        response = self.client.get('/task/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/task/1')

    def test_user_cannot_access_other_users_tasks(self):
        self.client.force_login(self.user2)
        response = self.client.get('/task/1')
        self.assertEqual(response.status_code, 403)

class TagDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('foo', 'foo@email.com', '123456')
        cls.user2 = User.objects.create_user('bar', 'bar@email.com', '123456')
        Tag.objects.create(
            name='user1 tag',
            user=cls.user1
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user1)
        response = self.client.get('/tag/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('tag-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user1)
        response = self.client.get('/tag/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/tag_detail.html')

    def test_non_logged_in_cannot_access_tags(self):
        response = self.client.get('/tag/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/tag/1')

    def test_user_cannot_access_other_users_tags(self):
        self.client.force_login(self.user2)
        response = self.client.get('/tag/1')
        self.assertEqual(response.status_code, 403)


class BookmarkOpsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('foo', 'foo@email.com', '123456')
        cls.user2 = User.objects.create_user('bar', 'bar@email.com', '123456')

    def test_non_logged_user_cannot_do_anything(self):
        response = self.client.get('/bookmark/create/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/bookmark/1/update/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/bookmark/1/delete/')
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_manipulate_other_users_bookmarks(self):
        Bookmark.objects.create(title='bookmark1', descr='descr', url='https://example.com', user=self.user1)
        self.client.force_login(self.user2)
        response = self.client.get('/bookmark/1/update/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/bookmark/1/delete/')
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        self.client.force_login(self.user1)
        response = self.client.get('/bookmark/create/')
        self.assertTemplateUsed(response, 'bookmark_form.html')
        self.assertEqual(response.status_code, 200)
        data = {
            'title': 'bookmark title',
            'descr': 'bookmark description',
            'url': 'https://example.com',
            'tags': [],
        }
        post_response = self.client.post('/bookmark/create/', data)
        self.assertRedirects(post_response, '/bookmark/1')

    def test_update(self):
        Bookmark.objects.create(title='bookmark1', descr='description', url='https://example.com', user=self.user1)
        self.client.force_login(self.user1)
        response = self.client.get('/bookmark/1/update/')
        self.assertTemplateUsed(response, 'bookmark_form.html')
        self.assertEqual(response.status_code, 200)
        data = {
            'title': 'foo',
            'descr': 'foo descr',
            'url': 'https://google.com',
            'tags': [],
        }
        post_response = self.client.post('/bookmark/1/update/', data)
        self.assertRedirects(post_response, '/bookmark/1')
        response = self.client.get('/bookmark/1')
        updated_bookmark = response.context['bookmark']
        self.assertEqual(updated_bookmark.title, 'foo')
        self.assertEqual(updated_bookmark.descr, 'foo descr')
        self.assertEqual(updated_bookmark.url, 'https://google.com')

    def test_delete(self):
        Bookmark.objects.create(title='bookmark1', descr='description', url='https://example.com', user=self.user1)
        self.client.force_login(self.user1)
        response = self.client.get('/bookmark/1/delete/')
        self.assertTemplateUsed(response, 'bookmark_confirm_delete.html')
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post('/bookmark/1/delete/')
        self.assertRedirects(post_response, '/bookmark/')


class TaskOpsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('foo', 'foo@email.com', '123456')
        cls.user2 = User.objects.create_user('bar', 'bar@email.com', '123456')

    def test_non_logged_user_cannot_do_anything(self):
        response = self.client.get('/task/create/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/task/1/update/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/task/1/delete/')
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_manipulate_other_users_tasks(self):
        Task.objects.create(name='task1', descr='descr', priority=1, due_date=timezone.now() + datetime.timedelta(days=1), user=self.user1)
        self.client.force_login(self.user2)
        response = self.client.get('/task/1/update/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/task/1/delete/')
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        self.client.force_login(self.user1)
        response = self.client.get('/task/create/')
        self.assertTemplateUsed(response, 'task_form.html')
        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'task name',
            'descr': 'task description',
            'priority': 1,
            'due_date': (timezone.now() + datetime.timedelta(days=1)).date(),
            'due_time': datetime.time(hour=2, minute=0),
            'tags': [],
        }
        post_response = self.client.post('/task/create/', data)
        self.assertRedirects(post_response, '/task/1')

    def test_update(self):
        Task.objects.create(name='task1', descr='description', priority=1, due_date=timezone.now() + datetime.timedelta(days=1), user=self.user1)
        self.client.force_login(self.user1)
        response = self.client.get('/task/1/update/')
        self.assertTemplateUsed(response, 'task_form.html')
        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'foo',
            'descr': 'foo descr',
            'priority': 2,
            'due_date': (timezone.now() + datetime.timedelta(days=1)).date(),
            'due_time': datetime.time(hour=2, minute=0),
            'tags': [],
        }
        post_response = self.client.post('/task/1/update/', data)
        self.assertRedirects(post_response, '/task/1')
        response = self.client.get('/task/1')
        updated_task = response.context['task']
        self.assertEqual(updated_task.name, 'foo')
        self.assertEqual(updated_task.descr, 'foo descr')
        self.assertEqual(updated_task.priority, 2)

    def test_delete(self):
        Task.objects.create(name='task1', descr='description', priority=1, due_date=timezone.now() + datetime.timedelta(days=1), user=self.user1)
        self.client.force_login(self.user1)
        response = self.client.get('/task/1/delete/')
        self.assertTemplateUsed(response, 'task_confirm_delete.html')
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post('/task/1/delete/')
        self.assertRedirects(post_response, '/task/')


class TagOpsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('foo', 'foo@email.com', '123456')
        cls.user2 = User.objects.create_user('bar', 'bar@email.com', '123456')

    def test_non_logged_user_cannot_do_anything(self):
        response = self.client.get('/tag/create/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/tag/1/update/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/tag/1/delete/')
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_manipulate_other_users_tags(self):
        Tag.objects.create(name='task1', user=self.user1)
        self.client.force_login(self.user2)
        response = self.client.get('/tag/1/update/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/tag/1/delete/')
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        self.client.force_login(self.user1)
        response = self.client.get('/tag/create/')
        self.assertTemplateUsed(response, 'tag_form.html')
        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'tag name',
        }
        post_response = self.client.post('/tag/create/', data)
        self.assertRedirects(post_response, '/tag/1')

    def test_update(self):
        Tag.objects.create(name='tag1', user=self.user1)
        self.client.force_login(self.user1)
        response = self.client.get('/tag/1/update/')
        self.assertTemplateUsed(response, 'tag_form.html')
        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'foo',
        }
        post_response = self.client.post('/tag/1/update/', data)
        self.assertRedirects(post_response, '/tag/1')
        response = self.client.get('/tag/1')
        updated_tag = response.context['tag']
        self.assertEqual(updated_tag.name, 'foo')

    def test_delete(self):
        Tag.objects.create(name='tag1', user=self.user1)
        self.client.force_login(self.user1)
        response = self.client.get('/tag/1/delete/')
        self.assertTemplateUsed(response, 'tag_confirm_delete.html')
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post('/tag/1/delete/')
        self.assertRedirects(post_response, '/tag/')

