from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    # path('register/', views.register_view, name='register'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('diary/', views.diary, name='diary'),
    path('add-entry/', views.add_entry, name='add_entry'),
    path('add-goal/', views.add_goal, name='add_goal'),
    path('goal/<int:goal_id>/completed/', views.mark_goal_as_completed, name='mark_goal_as_completed'),
    path('goal/<int:goal_id>/uncompleted/', views.mark_goal_as_uncompleted, name='mark_goal_as_uncompleted'),
    path('goal/<int:goal_id>/archive/', views.archive_goal, name='archive_goal'),
    path('goal/<int:goal_id>/unarchive/', views.unarchive_goal, name='unarchive_goal'),
    path('goal/<int:goal_id>/edit', goal_edit, name='goal_edit'),
    path('entry/<int:entry_id>/edit', entry_edit, name='entry_edit'),
    path('archive/', views.archive_view, name='archive'),

    path('task_add', task_add, name='task_add'),
    path('goal/tasks/<int:task_id>/complete', task_complete, name='task_complete'),
    path('goal/tasks/<int:task_id>/uncomplete', task_uncomplete, name='task_uncomplete'),

]
