from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DayEntry, Goal, Task
from .forms import DayEntryForm, GoalForm, TaskAddForm, RegisterForm, FeedbackAddForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'diary/home.html')

"""предыдущая форма регистрации, сейчас не используется"""
def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        # Здесь можно добавить логику для автоматического входа
        return redirect('login')  # Перенаправление после успешной регистрации

    context = {
        'form': form,
        'title': 'Регистрация',
        'button_text': 'Зарегистрироваться',
    }
    return render(request, 'diary/auth_form.html', context)

def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('diary')  # Перенаправление после успешного входа

    context = {
        'form': form,
        'title': 'Вход',
        'button_text': 'Войти',
    }
    return render(request, 'diary/auth_form.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def diary(request):
    goals = Goal.objects.filter(user=request.user, is_archived=False)
    entries = DayEntry.objects.filter(user=request.user)

    # Если форма для создания цели была отправлена
    if request.method == 'POST' and 'create_goal' in request.POST:
        goal_form = GoalForm(request.POST)
        if goal_form.is_valid():
            goal = goal_form.save(commit=False)
            goal.user = request.user  # Привязываем цель к текущему пользователю
            goal.save()
            return redirect('diary')
    else:
        goal_form = GoalForm()

    # Если форма для добавления записи в дневник была отправлена
    if request.method == 'POST' and 'create_entry' in request.POST:
        entry_form = DayEntryForm(request.POST)
        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            entry.user = request.user  # Привязываем запись к текущему пользователю
            entry.save()
            return redirect('diary')
    else:
        entry_form = DayEntryForm()


    entries_paginator = Paginator(entries, 3)
    entries_page_number = request.GET.get('page', 1)
    entries_page_obj = entries_paginator.get_page(entries_page_number)

    task_form=TaskAddForm()
    tasks = Task.objects.all()


    return render(request, 'diary/diary.html', {
        'goal_form': goal_form,
        'entry_form': entry_form,
        'goals': goals,
        'entries': entries,
        'page_obj': entries_page_obj,
        'task_form': task_form,
        'tasks':tasks,
    })

@login_required
def add_entry(request):
    if request.method == 'POST':
        form = DayEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('diary')
    else:
        form = DayEntryForm()
    return render(request, 'diary/add_entry.html', {'form': form})

@login_required
def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('diary')
    else:
        form = GoalForm()
    return render(request, 'diary/add_goal.html', {'form': form})

def mark_goal_as_completed(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.is_completed = True
    goal.save()
    return redirect('diary')  # Перенаправление на страницу дневника

def mark_goal_as_uncompleted(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.is_completed = False
    goal.save()
    return redirect('diary')  # Перенаправление на страницу дневника

def archive_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.is_archived = True
    goal.save()
    return redirect('archive')  # Перенаправление на страницу архива

def unarchive_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.is_archived = False
    goal.save()
    return redirect('diary')  # Перенаправление на страницу дневника

def archive_view(request):
    archived_goals = Goal.objects.filter(user=request.user, is_archived=True)
    return render(request, 'diary/archive.html', {'archived_goals': archived_goals})



# РЕДАКТИРОВАНИЕ ПОСТОВ
@login_required
def goal_edit(request, goal_id):

    goal = Goal.objects.get(id=goal_id) # получили объект из базы

    form = GoalForm(instance=goal) # создали форму как обычно, но получили инстанс

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal) # instance - привязка к старой записи
        if form.is_valid():
            # обновление объекта
            form.save()
            return redirect('diary')  # Перенаправляем на страницу дневника
        else:
            form = GoalForm(instance=goal)

    return render(request, 'diary/goal_edit.html', {"form":form}) # передали эту форму в контексте

@login_required
def entry_edit(request, entry_id):

    entry = DayEntry.objects.get(id=entry_id) # получили объект из базы

    form = DayEntryForm(instance=entry) # создали форму как обычно, но получили инстанс

    if request.method == 'POST':
        form = DayEntryForm(request.POST, instance=entry) # instance - привязка к старой записи
        if form.is_valid():
            # обновление объекта
            form.save()
            return redirect('diary')  # Перенаправляем на страницу дневника
        else:
            form = DayEntryForm(instance=entry)

    return render(request, 'diary/entry_edit.html', {"form":form}) # передали эту форму в контексте


def task_add(request):

    if request.method == 'POST':
        form = TaskAddForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            project = request.POST['project']
            project = Goal.objects.get(id=project)

            Task.objects.create(title=title,
                                project=project
                                )
            return redirect('diary')


def task_del(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()

    return redirect('diary')

def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.status = Task.COMPLETED
    task.save()

    return redirect('diary')

def task_uncomplete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.status = Task.UNCOMPLETED
    task.save()

    return redirect('diary')


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('Надо создать пользователя')

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            User = get_user_model()
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            user = authenticate(request, username=username, password=password)
            login(request=request, user=user)

            return redirect('diary')

    context = {
        'form': form,
        'title': 'Регистрация',
        'button_text': 'Зарегистрироваться',
    }

    return render(request, 'diary/auth_form.html', context)



def feedback_add(request):
    form = FeedbackAddForm()
    if request.method == "POST":
        form = FeedbackAddForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('feedback_done')

    context = {
        'form' : form
    }

    return render(request, 'diary/contacts.html', context)



def feedback_done(request):
    return render(request, 'diary/feedback_done.html')

