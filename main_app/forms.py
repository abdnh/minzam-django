from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Tag, User, ensure_future_date

class BookmarkForm(forms.Form):

    title = forms.CharField(max_length=255, label="عنوان")
    descr = forms.CharField(widget=forms.Textarea, label='وصف', required=False)
    url = forms.URLField(label="رابط")
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects, label='وسوم', required=False)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(user=user)

class DateTimeWidget(forms.DateInput):
    input_type = 'datetime-local'

    def __init__(self, format=None):
        attrs = {
            # for browsers that do not support datetime-local
            'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}'
        }
        super().__init__(attrs, format)


class TaskForm(forms.Form):

    name = forms.CharField(label='اسم')
    descr = forms.CharField(widget=forms.Textarea, label='وصف', required=False)
    priority = forms.IntegerField(label='أولوية', min_value=0)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects, label='وسوم', required=False)
    due_date = forms.DateTimeField(widget=DateTimeWidget, label='تاريخ الاستحقاق', validators=[ensure_future_date])

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
