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
    class Meta:
        model = TimeEntry
        fields = '__all__'


class TimeEntryTypeList(DjangoObjectType):
    class Meta:
        model = TimeEntry
        filterset_class = TimeEntryFilter


class Query(object):
    taskgroup = graphene.Field(TaskGroupType)
    taskgroup_list = DjangoFilterListField(TaskGroupListType)
    task = DjangoObjectField(TaskType)
    task_list = DjangoFilterListField(TaskListType)
    timeentry = DjangoObjectField(TimeEntryType)
    timeentry_list = DjangoFilterListField(TimeEntryTypeList)
    