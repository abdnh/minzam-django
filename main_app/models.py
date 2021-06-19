from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


MAX_NAME_LEN = 255

class Tag(models.Model):
    name = models.CharField(verbose_name='اسم', max_length=MAX_NAME_LEN)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('tag-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"



class Bookmark(models.Model):

    title = models.CharField(verbose_name='عنوان', max_length=MAX_NAME_LEN)
    descr = models.TextField(verbose_name='وصف')
    url = models.URLField(verbose_name='رابط')
    tags = models.ManyToManyField(Tag, verbose_name='وسوم', blank=True)
    created = models.DateTimeField(null=True, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('bookmark-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.title}"


def ensure_future_date(value):
    if value <= timezone.now():
        raise ValidationError(
            '%(value)s هو تاريخ مضى وانتهى',
            params={'value': value},
        )


class Task(models.Model):

    name = models.CharField(verbose_name='اسم', max_length=MAX_NAME_LEN)
    descr = models.TextField(verbose_name='وصف')
    priority = models.IntegerField(verbose_name='أولوية')
    tags = models.ManyToManyField(Tag, verbose_name='وسوم', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(validators=[ensure_future_date])
    notified = models.BooleanField(verbose_name='تم التنبيه', default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['due_date', 'priority']

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"

