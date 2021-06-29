import sys, datetime, threading, json

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

import requests

def send_email_via_trustifi(subject, html_body, recipient):

    payload = {
        "recipients": [
            {
                "email": recipient
            }
        ],
        "title": subject,
        "html": html_body,
    }

    headers = {
    'x-trustifi-key': settings.TRUSTIFI_KEY,
    'x-trustifi-secret': settings.TRUSTIFI_SECRET,
    'Content-Type': 'application/json'
    }

    response = requests.request('POST', 'https://be.trustifi.com/api/i/v1/email', headers = headers, data = json.dumps(payload))
    print(response.json())


def send_task_notifications(Task):
    domain = settings.BASE_URL

    for task in Task.objects.filter(notified=False, due_date__lte=timezone.now()):
        url = f"{domain}{task.get_absolute_url()}"
        subject = f'منظام - حان آوان مهمتك "{task.name}"'
        context = {'task_name': task.name, 'task_url': url}
        text_body = loader.render_to_string('task_notification_body.txt', context)
        html_body = loader.render_to_string('task_notification_body.html', context)
        recipient = task.user.email
        print(f'- sending email to "{task.user.email}" about task "{task.name}"')
        if settings.USE_TRUSTIFI:
            send_email_via_trustifi(subject, html_body, recipient)
        else:
            send_mail(subject, text_body, None, [recipient], fail_silently=False, html_message=html_body)

        task.notified = True
        task.save()


def run_task_notifier():
    from .models import Task

    exit = threading.Event()

    def notify():
        while True:
            s = exit.wait(60)
            if s:
                break
            exit.clear()
            print(f"{datetime.datetime.now()}: sending task notifications", file=sys.stderr)
            send_task_notifications(Task)

    threading.Thread(target=notify).start()

