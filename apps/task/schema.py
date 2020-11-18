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


TIME_ENTRY_ANNOTATE = Sum(
    F('end_time') - F('start_time'),
    output_field=DurationField(),
)

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

    class Meta:
        model = TimeEntry
        fields = '__all__'


class TimeEntryTypeList(DjangoObjectType):
    duration = graphene.String()

    class Meta:
        model = TimeEntry
        filterset_class = TimeEntryFilter


class SummaryType(graphene.ObjectType):
    total_hours = graphene.String()
    total_hours_day = graphene.List(TimeEntryType)


class Query(object):
    taskgroup = graphene.Field(TaskGroupType)
    taskgroup_list = DjangoFilterListField(TaskGroupListType)
    task = DjangoObjectField(TaskType)
    task_user = graphene.List(TaskType)
    task_list = DjangoFilterListField(TaskListType)
    timeentry = DjangoObjectField(TimeEntryType)
    summary = graphene.Field(SummaryType, date_from=graphene.Date(),
                             date_to=graphene.Date())

    def resolve_task_user(root, info):
        user = info.context.user
        if not user:
            return None
        else:
            return Task.objects.filter(
                user=user,
            )

    def resolve_summary(root, info, **kwargs):
        date_from_at = kwargs.get('date_from', None)
        date_to_at = kwargs.get('date_to', None)
        user = info.context.user
        if not user:
            return None
        else:
            # gives the filter day total time
            queryset = TimeEntry.objects.filter(
                user=user,
                date__gte=date_from_at,
                date__lte=date_to_at
            ).distinct().annotate(
                duration=F('end_time') - F('start_time')
            ).aggregate(
                total_duration=Sum('duration')
            )['total_duration']

            # for the particular day totaltime
            queryset_day = TimeEntry.objects.filter(
                user=user
            ).order_by('date').values('date').annotate(
                duration=F('end_time') - F('start_time')
            ).aggregate(
                total_duration=Sum('duration')
            )['total_duration']
            print(queryset_day)
            return SummaryType(
                total_hours=queryset,
                total_hours_day=queryset_day
            )
