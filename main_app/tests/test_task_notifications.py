from datetime import timedelta
import time

from django.utils import timezone
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from main_app.models import Task
from main_app.task_notifier import send_task_notifications

class TaskNotifierTest(TestCase):

    def test_task_notifier(self):
        settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        user1 = User.objects.create_user('foo', 'abdalkader.n2000@gmail.com', '123456')
        num_of_tasks = 4
        for i in range(num_of_tasks-1):
            Task.objects.create(name=f'task {i+1}', descr='some description', priority=1, due_date=timezone.now(), user=user1)
        Task.objects.create(name=f'task {num_of_tasks}', descr='some description', priority=1, due_date=timezone.now() + timedelta(days=1), user=user1)
        time.sleep(1)
        send_task_notifications(Task)
        for i in range(num_of_tasks-1):
            task = Task.objects.get(id=i+1)
            self.assertTrue(task.notified)
        task = Task.objects.get(id=num_of_tasks)
        self.assertFalse(task.notified)
