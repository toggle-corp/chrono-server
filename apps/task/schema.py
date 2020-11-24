import datetime
from dateutil.relativedelta import relativedelta


from django.db.models import F, Sum, DurationField
from django.utils.timezone import now

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
from project.schema import ProjectType
from project.models import Project


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
    duration = graphene.String()
    task_list = graphene.List(TimeEntryType)

    def resolve_task_list(root, info, **kwargs):
        date = root.get('date', None)
        user = info.context.user
        queryset = TimeEntry.objects.filter(
                user=user,
                date=date
        )
        return queryset


class SummaryWeekType(graphene.ObjectType):
    total_hours_weekly = graphene.String()
    total_hours_day = graphene.List(SummaryDay)


class SummaryMonthType(graphene.ObjectType):
    total_hours_monthly = graphene.String()
    total_hours_day = graphene.List(SummaryDay)


class SummaryWeekDashBoard(graphene.ObjectType):
    total_hours = graphene.String()
    total_hours_day = graphene.List(SummaryDay)


class DashBoardType(graphene.ObjectType):
    this_week = graphene.Field(SummaryWeekDashBoard)
    """project_total = graphene.String()
    project_individual = graphene.List(ProjectType)"""

    def resolve_this_week(root, info, *a, **k):
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(6)
        user = info.context.user
        root = TimeEntry.objects.filter(
            user=info.context.user,
            date__range=[start_week, end_week]
        ).order_by().values('date')
        if user.is_authenticated:
            # week total duration
            hours_week = root.annotate(
                duration=F('end_time') - F('start_time'),
            )
            return SummaryWeekDashBoard(
                total_hours=hours_week.aggregate(sum=Sum('duration'))['sum'],
                total_hours_day=hours_week
            )
        else:
            return None


class Query(object):
    taskgroup = graphene.Field(TaskGroupType)
    taskgroup_list = DjangoFilterListField(TaskGroupListType)
    task = DjangoObjectField(TaskType)
    task_user = graphene.List(TaskType)
    task_list = DjangoFilterListField(TaskListType)
    timeentry = DjangoObjectField(TimeEntryType)
    summary_weekly = graphene.Field(SummaryWeekType)
    summary_monthly = graphene.Field(SummaryMonthType)
    dashboard = graphene.Field(DashBoardType)

    def resolve_task_user(root, info):
        user = info.context.user
        if not user:
            return None
        else:
            return Task.objects.filter(
                user=user,
            )

    def resolve_summary_weekly(root, info, **kwargs):
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(6)
        user = info.context.user
        if user.is_authenticated:
            # week total duration
            hours_week = TimeEntry.objects.filter(
                user=user,
                date__range=[start_week, end_week]
            ).order_by().values('date').annotate(
                duration=F('end_time') - F('start_time'),
            ).aggregate(
                total_duration=Sum(F('duration'))
            )['total_duration']

            # day total_duration
            hours_day = TimeEntry.objects.filter(
                user=user,
                date__range=[start_week, end_week]
            ).values('date').order_by('date').annotate(
                duration_day=Sum(F('end_time') - F('start_time'))
            ).values('date', 'duration_day')

            return SummaryWeekType(
                total_hours_weekly=hours_week,
                total_hours_day=hours_day,
            )
        else:
            return None

    def resolve_summary_monthly(root, info, **kwargs):
        date = datetime.date.today()
        last_day = date + relativedelta(day=1, months=+1, days=-1)
        first_day = date + relativedelta(day=1)
        user = info.context.user
        if user.is_authenticated:

            # monthly total_duration
            hours_monthly = TimeEntry.objects.filter(
                user=user,
                date__gte=first_day,
                date__lte=last_day,
            ).values('date').order_by().annotate(
                duration=F('end_time') - F('start_time'),
            ).aggregate(
                total_duration=Sum(F('duration'))
            )['total_duration']

            # day total_duration
            hours_day = TimeEntry.objects.filter(
                user=user,
                date__gte=first_day,
                date__lte=last_day,
            ).values('date').order_by('date').annotate(
                duration_day=Sum(F('end_time') - F('start_time'))
            ).values('date', 'duration_day')

            return SummaryMonthType(
                total_hours_monthly=hours_monthly,
                total_hours_day=hours_day
            )
        else:
            return None

    # TODO: Remove one
    def resolve_dashboard(root, info, **kwargs):
        return DashBoardType()

    def resolve_dashboard_1(root, info, **kwargs):
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(6)
        return TimeEntry.objects.filter(
                user=info.context.user,
                date__range=[start_week, end_week]
            ).order_by().values('date')
