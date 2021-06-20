from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Tag, User

class BookmarkForm(forms.Form):

    title = forms.CharField(max_length=255, label="عنوان")
    descr = forms.CharField(widget=forms.Textarea, label='وصف', required=False)
    url = forms.URLField(label="رابط")
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects, label='وسوم', required=False)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(user=user)


class DateWidget(forms.DateInput):
    input_type = 'date'

class TimeWidget(forms.TimeInput):
    input_type = 'time'


def validate_due_date(value):
    if value < timezone.now().date():
        raise ValidationError(
            '%(value)s هو تاريخ مضى وانتهى',
            params={'value': value},
        )


class TaskForm(forms.Form):

    name = forms.CharField(label='اسم')
    descr = forms.CharField(widget=forms.Textarea, label='وصف', required=False)
    priority = forms.IntegerField(label='أولوية', min_value=1, help_text='مدى أهمية المهمة لك - المهام ذات القيم الأصغر تعد أهم')
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects, label='وسوم', required=False)
    due_date = forms.DateField(widget=DateWidget, label='تاريخ الاستحقاق', validators=[validate_due_date])
    due_time = forms.TimeField(widget=TimeWidget, label='ساعة الاستحقاق')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(user=user)


class TagForm(forms.Form):

    name = forms.CharField(label='اسم')


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(label='بريد إلكتروني')

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
