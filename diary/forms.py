from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import DayEntry, Goal

class DayEntryForm(forms.ModelForm):
    class Meta:
        model = DayEntry
        fields = ['gratitude', 'achievements', 'thoughts']
        widgets = {
            'gratitude': forms.Textarea(attrs={'placeholder': 'Напишите 3 пункта благодарности'}),
            'achievements': forms.Textarea(attrs={'placeholder': 'Напишите 3 достижения'}),
            'thoughts': forms.Textarea(attrs={'placeholder': 'Что сработало хорошо? Что можно улучшить? Какие планы на следующий день?'}),
        }

        def __init__(self, *args, **kwargs):
            super(DayEntryForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description']

        def __init__(self, *args, **kwargs):
            super(GoalForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'

class GoalStatusForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['is_completed']

        def __init__(self, *args, **kwargs):
            super(GoalStatusForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'


class TaskAddForm(forms.Form):
    title = forms.CharField(max_length=500, label='')

    def __init__(self, *args, **kwargs):
        super(TaskAddForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise ValidationError('Пароли не совпадают')

        return password2

    # валидация на юзернейм
    def clean_username(self):
        username = self.cleaned_data['username']
        User = get_user_model()

        if User.objects.filter(username=username).exists():
            raise ValidationError('Такой пользователь уже есть')

        return username

