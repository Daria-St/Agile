from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, которому принадлежит цель
    title = models.CharField(max_length=255)  # Заголовок цели
    description = models.TextField()  # Описание цели
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    is_completed = models.BooleanField(default=False)  # Статус выполнения
    is_archived = models.BooleanField(default=False)  # Архивирование

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def __str__(self):
        return self.title

class DayEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    gratitude = models.TextField()
    achievements = models.TextField()
    thoughts = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ["-date"]

    def __str__(self):
        return f"Entry for {self.date} by {self.user.username}"


class Task(models.Model):

    COMPLETED = 'Completed'
    UNCOMPLETED = 'Uncompleted'

    TASK_STATUS = [
        (COMPLETED, 'Выполнена'),
        (UNCOMPLETED, 'Не выполнена'),
    ]
    title = models.CharField(max_length=500)
    project = models.ForeignKey(
        Goal,
        on_delete=models.SET_NULL,
        blank = True,
        null=True,
        related_name='tasks'
    )

    status = models.CharField(max_length=100, default=UNCOMPLETED, choices=TASK_STATUS)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title



class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.TextField()

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return self.name