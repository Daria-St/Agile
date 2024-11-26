from django.contrib import admin


from .models import *
admin.site.register(Goal)
admin.site.register(DayEntry)
admin.site.register(Task)
