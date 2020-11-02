import django_filters

from task.models import Task, TaskGroup, TimeEntry


class TaskFilter(django_filters.FilterSet):
    title_contains = django_filters.CharFilter(
                     field_name='title',
                     lookup_expr='icontains'
    )

    class Meta:
        model = Task
        fields = ['task_group', 'user']


class TaskGroupFilter(django_filters.FilterSet):
    title_contains = django_filters.CharFilter(
                     field_name='title',
                     lookup_expr='icontains'
    )

    class Meta:
        model = TaskGroup
        fields = {
            "start_date": ("lte", "gte"),
            "end_date": ("lte", "gte"),
        }


class TimeEntryFilter(django_filters.FilterSet):
    class Meta:
        model = TimeEntry
        fields = {
            "task": ("exact", ),
            "user": ("exact", ),
        }
