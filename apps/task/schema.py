import datetime
from dateutil.relativedelta import relativedelta

from django.db.models import F, Sum
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
from project.models import Project


class TaskGroupType(DjangoObjectType):
    status = graphene.Field(StatusGrapheneEnum)
    duration = graphene.String()

    class Meta:
        model = TaskGroup
        fields = '__all__'

    def resolve_duration(self, info, **kwargs):
        user = info.context.user
        if not user:
            return None
        else:
            return self.duration_taskgroup(user)

class TaskGroupListType(DjangoObjectType):
    class Meta:
        model = TaskGroup
        filterset_class = TaskGroupFilter


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = '__all__'

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class TaskListType(DjangoObjectType):
    duration = graphene.String()

    class Meta:
        model = Task
        filterset_class = TaskFilter

    def resolve_duration(self, info, **kwargs):
        user = info.context.user
        if not user:
            return None
        else:
            return self.duration_task(user)

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


class ProjectDetail(graphene.ObjectType):
    duration = graphene.String()
    project_name = graphene.String()


class DashBoardMyProject(graphene.ObjectType):
    project_name = graphene.String()
    client_name = graphene.String()
    edited_on = graphene.Date()
    status = graphene.String()
    hours_spent = graphene.String()


class SummaryWeekType(graphene.ObjectType):
    total_hours_weekly = graphene.String()
    total_hours_day = graphene.List(SummaryDay)


class SummaryMonthType(graphene.ObjectType):
    total_hours_monthly = graphene.String()
    total_hours_day = graphene.List(SummaryDay)


class SummaryWeekDashBoard(graphene.ObjectType):
    total_hours = graphene.String()
    total_hours_day = graphene.List(SummaryDay)


class SummaryProjectDashBoard(graphene.ObjectType):
    project_total = graphene.String()
    project_particular = graphene.List(ProjectDetail)


class SummaryMostActiveProject(graphene.ObjectType):
    project_total = graphene.String()
    project_particular = graphene.List(ProjectDetail)


class DashBoardType(graphene.ObjectType):
    this_week = graphene.Field(SummaryWeekDashBoard)
    hours_by_project = graphene.Field(SummaryProjectDashBoard)
    most_active_project = graphene.Field(SummaryMostActiveProject)
    my_project = graphene.List(DashBoardMyProject)

    def resolve_this_week(root, info, *args, **kwargs):
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(6)
        user = info.context.user
        queryset = TimeEntry.objects.filter(
            user=info.context.user,
            date__range=[start_week, end_week]
        ).order_by().values('date')
        if user.is_authenticated:
            # week total duration
            hours_week = queryset.annotate(
                duration=F('end_time') - F('start_time'),
            ).aggregate(sum=Sum('duration'))['sum']

            hours_day = queryset.annotate(
                duration=Sum(F('end_time') - F('start_time'))
            )
            return SummaryWeekDashBoard(
                total_hours=hours_week,
                total_hours_day=hours_day
            )
        else:
            return None

    def resolve_hours_by_project(root, info, *args, **kwargs):
        user = info.context.user
        if not user:
            return None
        else:
            # get the project for the user
            projects = Project.get_for(user)
            queryset = TimeEntry.objects.filter(
                user=user,
                task__task_group__project__in=projects
            )
            total_project_hours = queryset.annotate(
                duration=F('end_time') - F('start_time'),
            ).aggregate(sum=Sum('duration'))['sum']

            each_project_hours = queryset.order_by().values('task__task_group__project').annotate(
                duration=Sum(F('end_time') - F('start_time')),
            ).values('duration', project_name=F('task__task_group__project__title'))

            return SummaryProjectDashBoard(
                project_total=total_project_hours,
                project_particular=each_project_hours
            )

    def resolve_most_active_project(root, info, *args, **kwargs):
        # gives the most active project in the week
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(6)
        user = info.context.user
        if not user:
            return None
        else:
            # get the project for the user
            projects = Project.get_for(user)
            queryset = TimeEntry.objects.filter(
                user=user,
                task__task_group__project__in=projects,
                date__lte=end_week,
                date__gte=start_week
            )
            total_project_hours = queryset.annotate(
                duration=F('end_time') - F('start_time'),
            ).aggregate(sum=Sum('duration'))['sum']

            each_project_hours = queryset.order_by().values('task__task_group__project').annotate(
                duration=Sum(F('end_time') - F('start_time')),
            ).values('duration', project_name=F('task__task_group__project__title'))

            return SummaryMostActiveProject(
                project_total=total_project_hours,
                project_particular=each_project_hours
            )

    def resolve_my_project(root, info, *args, **kwargs):
        user = info.context.user
        if not user:
            return None
        else:
            # get the projects for the user
            projects = Project.get_for(user=user)
            queryset = TimeEntry.objects.filter(
                task__task_group__project__in=projects
            ).order_by('task__task_group__project').values('task__task_group__project').annotate(
                duration=Sum(F('end_time') - F('start_time'))
            ).values(
                hours_spent=F('duration'),
                project_name=F('task__task_group__project__title'),
                client_name=F('task__task_group__project__client__name'),
                edited_on=F('task__task_group__project__modified_at'),
                status=F('task__task_group__status')
                )
            return queryset


class Query(object):
    taskgroup = DjangoObjectField(TaskGroupType)
    taskgroup_list = DjangoFilterListField(TaskGroupListType)
    task = DjangoObjectField(TaskType)
    task_user = graphene.List(TaskType)
    task_list = DjangoFilterListField(TaskListType)
    timeentry = DjangoObjectField(TimeEntryType)
    summary_weekly = graphene.Field(SummaryWeekType)
    summary_monthly = graphene.Field(SummaryMonthType)
    dashboard = graphene.Field(DashBoardType)

    def resolve_taskgroup(root, info, **kwargs):
        user = info.context.user
        if not user:
            return None
        else:
            return TaskGroup.objects.filter(
                users=user
            )

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
                duration=Sum(F('end_time') - F('start_time'))
            ).values('date', 'duration')

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
                duration=Sum(F('end_time') - F('start_time'))
            ).values('date', 'duration')

            return SummaryMonthType(
                total_hours_monthly=hours_monthly,
                total_hours_day=hours_day
            )
        else:
            return None

    def resolve_dashboard(root, info, **kwargs):
        return DashBoardType()
