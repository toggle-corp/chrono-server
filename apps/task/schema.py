import datetime

from django.db.models import F, Sum, DurationField

import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import (
    DjangoObjectField,
    DjangoObjectType,
    DjangoFilterListField,
)
#from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from user.schema import UserType
from usergroup.schema import UserGroupType
from task.models import TaskGroup, Task, TimeEntry
from task.enums import StatusGrapheneEnum
from task.filters import TaskFilter, TaskGroupFilter, TimeEntryFilter


class TaskGroupType(DjangoObjectType):
    class Meta:
        model = TaskGroup
        fields = '__all__'

    status = graphene.Field(StatusGrapheneEnum)


class TaskGroupListType(DjangoObjectType):
    class Meta:
        model = TaskGroup
        filterset_class = TaskGroupFilter


class TaskType(DjangoObjectType):

    class Meta:
        model = Task
        fields = '__all__'


class TaskListType(DjangoObjectType):
    class Meta:
        model = Task
        filterset_class = TaskFilter


class TimeEntryType(DjangoObjectType):
    duration = graphene.String()
    day_total = graphene.String()

    class Meta:
        model = TimeEntry
        fields = '__all__'


class TimeEntryTypeList(DjangoObjectType):
    duration = graphene.String()

    class Meta:
        model = TimeEntry
        filterset_class = TimeEntryFilter


class SummaryDay(graphene.ObjectType):
    date = graphene.Date()
    duration_day = graphene.String()
    task_list = graphene.List(TimeEntryType)

    def resolve_task_list(root, info, **kwargs):
        date = root.get('date', None)
        user = info.context.user
        queryset = TimeEntry.objects.filter(
                user=user,
                date=date
        )
        return queryset


class SummaryType(graphene.ObjectType):
    total_hours = graphene.String()
    total_hours_day = graphene.List(SummaryDay)


class Query(object):
    taskgroup = graphene.Field(TaskGroupType)
    taskgroup_list = DjangoFilterListField(TaskGroupListType)
    task = DjangoObjectField(TaskType)
    task_user = graphene.List(TaskType)
    task_list = DjangoFilterListField(TaskListType)
    timeentry = DjangoObjectField(TimeEntryType)
    summary = graphene.Field(SummaryType)

    def resolve_task_user(root, info):
        user = info.context.user
        if not user:
            return None
        else:
            return Task.objects.filter(
                user=user,
            )

    def resolve_summary(root, info, **kwargs):
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(6)
        user = info.context.user
        if user.is_authenticated:
            # week total duration
            queryset_week = TimeEntry.objects.filter(
                user=user,
                date__range=[start_week, end_week]
            ).order_by().values('date').annotate(
                duration=F('end_time') - F('start_time'),
            ).aggregate(
                total_duration=Sum(F('duration'))
            )['total_duration']

            # day total_duration
            queryset_day = TimeEntry.objects.filter(
                user=user,
                date__range=[start_week, end_week]
            ).values('date').order_by('date').annotate(
                duration_day=Sum(F('end_time') - F('start_time'))
            ).values('date', 'duration_day')

            return SummaryType(
                total_hours=queryset_week,
                total_hours_day=queryset_day
            )
        else:
            return None
