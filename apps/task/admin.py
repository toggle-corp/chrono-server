from django.contrib import admin

from .models import Task, TimeEntry, TaskGroup

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
    pass
