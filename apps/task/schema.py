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


class TaskGroupType(DjangoObjectType):
    class Meta:
        model = TaskGroup
        fields = '__all__'

    status = graphene.Field(StatusGrapheneEnum)


class TaskGroupListType(DjangoObjectType):
    class Meta:
        model = TaskGroup
        filter_fields = {
            "title": ("icontains", ),
            "start_date": ("lte", "gte"),
            "end_date": ("lte", "gte"),
        }


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = '__all__'


class TaskListType(DjangoObjectType):
    class Meta:
        model = Task
        filter_fields = {
            "id": ("exact", ),
            "title": ("icontains", ),
            "user": ("exact", ),
            "task_group": ("exact", )
        }


class TimeEntryType(DjangoObjectType):
    class Meta:
        model = TimeEntry
        fields = '__all__'


class TimeEntryTypeList(DjangoObjectType):
    class Meta:
        model = TimeEntry
        filter_fields = {
            "task": ("exact", ),
            "user": ("exact", ),
        }


class Query(object):
    taskgroup = graphene.Field(TaskGroupType)
    taskgroup_list = DjangoFilterListField(TaskGroupListType)
    task = DjangoObjectField(TaskType)
    task_list = DjangoFilterListField(TaskListType)
    timeentry = DjangoObjectField(TimeEntryType)
    timeentry_list = DjangoFilterListField(TimeEntryTypeList)
