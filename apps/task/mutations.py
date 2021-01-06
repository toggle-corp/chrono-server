from django.utils.translation import gettext
import graphene
from graphene_file_upload.scalars import Upload

from task.enums import StatusGrapheneEnum
from task.models import Task, TaskGroup, TimeEntry
from task.schema import (
    TaskGroupType,
    TaskGroupListType,
    TaskType,
    TaskListType,
    TimeEntryType,
)
from task.serializers import (
    TaskSerializer,
    TaskGroupSerializer,
    TimeEntrySerializer,
)
from utils.error_types import CustomErrorType, mutation_is_not_valid


class TaskCreateInputType(graphene.InputObjectType):
    """
    Task Create Input Type
    """

    title = graphene.String(required=True)
    description = graphene.String()
    external_url = graphene.String()
    task_group = graphene.ID()
    user = graphene.ID()
    created_by = graphene.ID()
    modified_by = graphene.ID()


class TaskUpdateInputType(graphene.InputObjectType):
    """
    Task Update Input Type
    """
    id = graphene.ID(required=True)
    title = graphene.String()
    task_group = graphene.ID()
    user = graphene.ID()


class TaskGroupCreateInputType(graphene.InputObjectType):
    """
    Task-Group Create Input Type
    """
    title = graphene.String(required=True)
    description = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    status = graphene.NonNull(StatusGrapheneEnum)
    users = graphene.List(graphene.ID, required=False)
    user_group = graphene.List(graphene.ID, required=False)
    created_by = graphene.ID()
    modified_by = graphene.ID()
    project = graphene.ID(required=True)


class TaskGroupUpdateInputType(graphene.InputObjectType):
    """
    Task-Group Update Input Type
    """
    id = graphene.ID(required=True)
    title = graphene.String()
    description = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    status = graphene.Field(StatusGrapheneEnum)
    users = graphene.List(graphene.ID)
    user_group = graphene.List(graphene.ID)
    project = graphene.ID()


class TimeEntryCreateInputType(graphene.InputObjectType):
    """
    Time Entry Create Input Type
    """
    description = graphene.String()
    date = graphene.Date()
    start_time = graphene.Time()
    end_time = graphene.Time()
    task = graphene.ID(required=True)
    user = graphene.ID()


class TimeEntryUpdateInputType(graphene.InputObjectType):
    """
    Time Entry Update Input Type
    """
    id = graphene.ID(required=True)
    date = graphene.Date()
    start_time = graphene.Time()
    end_time = graphene.Time()
    task = graphene.ID()
    user = graphene.ID()


class CreateTaskGroup(graphene.Mutation):
    class Arguments:
        data = TaskGroupCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TaskGroupType)

    @staticmethod
    def mutate(root, info, data):
        serializer = TaskGroupSerializer(data=data)
        if errors := mutation_is_not_valid(serializer):
            return CreateTaskGroup(errors=errors, ok=False)
        instance = serializer.save()
        return CreateTaskGroup(result=instance, errors=None, ok=True)


class UpdateTaskGroup(graphene.Mutation):
    class Arguments:
        data = TaskGroupUpdateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TaskGroupType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = TaskGroup.objects.get(id=data['id'])
        except TaskGroup.DoesNotExist:
            return UpdateTaskGroup(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=[gettext('TaskGroup does not exist.')])
            ])
        serializer = TaskGroupSerializer(instance=instance,
                                         data=data,
                                         partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return UpdateTaskGroup(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateTaskGroup(result=instance, errors=None, ok=True)


class DeleteTaskGroup(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TaskGroupType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = TaskGroup.objects.get(id=id)
        except TaskGroup.DoesNotExist:
            return DeleteTaskGroup(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=gettext('TaskGroup does not exist'))
            ])
        instance.delete()
        instance.id = id
        return DeleteTaskGroup(result=instance, errors=None, ok=True)


class CreateTask(graphene.Mutation):
    class Arguments:
        data = TaskCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, data):
        serializer = TaskSerializer(data=data)
        if errors := mutation_is_not_valid(serializer):
            return CreateTask(errors=errors, ok=False)
        instance = serializer.save()
        return CreateTask(result=instance, errors=None, ok=True)


class UpdateTask(graphene.Mutation):
    class Arguments:
        data = TaskUpdateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = Task.objects.get(id=data['id'])
        except Task.DoesNotExist:
            return UpdateTask(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=[gettext('Task does not exist.')])
            ])
        serializer = TaskSerializer(instance=instance,
                                    data=data,
                                    partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return UpdateTask(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateTask(result=instance, errors=None, ok=True)


class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return DeleteTask(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=gettext('Task does not exist'))
            ])
        instance.delete()
        instance.id = id
        return DeleteTask(result=instance, errors=None, ok=True)


class CreateTimeEntry(graphene.Mutation):
    class Arguments:
        data = TimeEntryCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TimeEntryType)

    @staticmethod
    def mutate(root, info, data):
        serializer = TimeEntrySerializer(data=data)
        if errors := mutation_is_not_valid(serializer):
            return CreateTimeEntry(errors=errors, ok=False)
        instance = serializer.save()
        return CreateTimeEntry(result=instance, errors=None, ok=True)


class UpdateTimeEntry(graphene.Mutation):
    class Arguments:
        data = TimeEntryUpdateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TimeEntryType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = TimeEntry.objects.get(id=data['id'])
        except TimeEntry.DoesNotExist:
            return UpdateTimeEntry(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=[gettext('UserGroup does not exist.')])
            ])
        serializer = TimeEntrySerializer(instance=instance,
                                         data=data,
                                         partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return UpdateTimeEntry(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateTimeEntry(result=instance, errors=None, ok=True)


class DeleteTimeEntry(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TimeEntryType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = TimeEntry.objects.get(id=id)
        except TimeEntry.DoesNotExist:
            return DeleteTimeEntry(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=gettext('Task does not exist'))
            ])
        instance.delete()
        instance.id = id
        return DeleteTimeEntry(result=instance, errors=None, ok=True)


class Mutation(object):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()
    create_taskGroup = CreateTaskGroup.Field()
    update_taskGroup = UpdateTaskGroup.Field()
    delete_taskGroup = DeleteTaskGroup.Field()
    create_timeEntry = CreateTimeEntry.Field()
    update_timeEntry = UpdateTimeEntry.Field()
    delete_timeEntry = DeleteTimeEntry.Field()
