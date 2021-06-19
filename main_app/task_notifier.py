import sys, datetime, threading, signal
from threading import Event

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

def send_task_notifications(Task):
    domain = settings.BASE_URL

    for task in Task.objects.filter(notified=False, due_date__lte=timezone.now()):
        url = f"{domain}{task.get_absolute_url()}"
        subject = f'منظام - حان آوان مهمتك "{task.name}"'
        context = {'task_name': task.name, 'task_url': url}
        text_body = loader.render_to_string('task_notification_body.txt', context)
        html_body = loader.render_to_string('task_notification_body.html', context)
        send_mail(subject, text_body, None, [task.user.email], fail_silently=False, html_message=html_body)
        task.notified = True
        task.save()


def run_task_notifier():
    if settings.TESTING:
        return

    exit = Event()

    def quit(s, f):
        exit.set()
        sys.exit()

    signal.signal(signal.SIGINT, quit)

    from .models import Task

    def foo():
        while True:
            s = exit.wait(60)
            if s:
                break
            exit.clear()
            print(f"{datetime.datetime.now()}: sending task notifications", file=sys.stderr)
            send_task_notifications(Task)

    threading.Thread(target=foo).start()

