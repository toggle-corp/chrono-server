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
        task_group = TaskGroupCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    task_group = graphene.Field(TaskGroupType)

    @staticmethod
    def mutate(root, info, task_group):
        serializer = TaskGroupSerializer(data=task_group)
        if errors := mutation_is_not_valid(serializer):
            return CreateTaskGroup(errors=errors, ok=False)
        instance = serializer.save()
        return CreateTaskGroup(task_group=instance, errors=None, ok=True)


class UpdateTaskGroup(graphene.Mutation):
    class Arguments:
        task_group = TaskGroupUpdateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    task_group = graphene.Field(TaskGroupType)

    @staticmethod
    def mutate(root, info, task_group):
        try:
            instance = TaskGroup.objects.get(id=task_group['id'])
        except TaskGroup.DoesNotExist:
            return UpdateTaskGroup(errors=[
                CustomErrorType(field='non_field_errors',
                                messages=[gettext('TaskGroup does not exist.')])
            ])
        serializer = TaskGroupSerializer(instance=instance,
                                         data=task_group,
                                         partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return UpdateTaskGroup(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateTaskGroup(task_group=instance, errors=None, ok=True)


class DeleteTaskGroup(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    task_group = graphene.Field(TaskGroupType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = TaskGroup.objects.get(id=id)
        except TaskGroup.DoesNotExist:
            return DeleteTaskGroup(errors=[
                CustomErrorType(field='non_field_errors', messages=gettext('TaskGroup does not exist'))
            ])
        instance.delete()
        instance.id = id
        return DeleteTaskGroup(task_group=instance, errors=None, ok=True)


class CreateTask(graphene.Mutation):
    class Arguments:
        task = TaskCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, task):
        serializer = TaskSerializer(data=task)
        if errors := mutation_is_not_valid(serializer):
            return CreateTask(errors=errors, ok=False)
        instance = serializer.save()
        return CreateTask(task=instance, errors=None, ok=True)


class UpdateTask(graphene.Mutation):
    class Arguments:
        task = TaskUpdateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, task):
        try:
            instance = Task.objects.get(id=task['id'])
        except Task.DoesNotExist:
            return UpdateTask(errors=[
                CustomErrorType(field='non_field_errors',
                                messages=[gettext('Task does not exist.')])
            ])
        serializer = TaskSerializer(instance=instance,
                                    data=task,
                                    partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return UpdateTask(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateTask(task=instance, errors=None, ok=True)


class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return DeleteTask(errors=[
                CustomErrorType(field='non_field_errors', messages=gettext('Task does not exist'))
            ])
        instance.delete()
        instance.id = id
        return DeleteTask(task=instance, errors=None, ok=True)


class CreateTimeEntry(graphene.Mutation):
    class Arguments:
        time_entry = TimeEntryCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    time_entry = graphene.Field(TimeEntryType)

    @staticmethod
    def mutate(root, info, time_entry):
        serializer = TimeEntrySerializer(data=time_entry)
        if errors := mutation_is_not_valid(serializer):
            return CreateTimeEntry(errors=errors, ok=False)
        instance = serializer.save()
        return CreateTimeEntry(time_entry=instance, errors=None, ok=True)


class UpdateTimeEntry(graphene.Mutation):
    class Arguments:
        time_entry = TimeEntryUpdateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    time_entry = graphene.Field(TimeEntryType)

    @staticmethod
    def mutate(root, info, time_entry):
        try:
            instance = TimeEntry.objects.get(id=time_entry['id'])
        except TimeEntry.DoesNotExist:
            return UpdateTimeEntry(errors=[
                CustomErrorType(field='non_field_errors',
                                messages=[gettext('UserGroup does not exist.')])
            ])
        serializer = TimeEntrySerializer(instance=instance,
                                         data=time_entry,
                                         partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return UpdateTimeEntry(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateTimeEntry(time_entry=instance, errors=None, ok=True)


class DeleteTimeEntry(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    time_entry = graphene.Field(TimeEntryType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = TimeEntry.objects.get(id=id)
        except TimeEntry.DoesNotExist:
            return DeleteTimeEntry(errors=[
                CustomErrorType(field='non_field_errors', messages=gettext('Task does not exist'))
            ])
        instance.delete()
        instance.id = id
        return DeleteTimeEntry(time_entry=instance, errors=None, ok=True)


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
