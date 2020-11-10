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
    start_date_lte = django_filters.CharFilter(
                     field_name='start_date',
                     lookup_expr='lte'
    )
    start_date_gte = django_filters.CharFilter(
                     field_name='start_date',
                     lookup_expr='gte'
    )
    end_date_lte = django_filters.CharFilter(
                     field_name='end_date',
                     lookup_expr='lte'
    )
    end_date_gte = django_filters.CharFilter(
                     field_name='end_date',
                     lookup_expr='gte'
    )

    class Meta:
        model = TaskGroup
        fields = ()


class TimeEntryFilter(django_filters.FilterSet):
    class Meta:
        model = TimeEntry
        fields = {
            "task": ("exact", ),
            "user": ("exact", ),
        }
