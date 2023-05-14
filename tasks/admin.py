from django.contrib import admin

# Register your models here.
from .models import Task,TaskStatus,TaskLevel


admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(TaskLevel)
