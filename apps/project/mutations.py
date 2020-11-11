from django.utils.translation import gettext

import graphene
from graphene_file_upload.scalars import Upload

from project.models import (
    Client,
    Project,
    Tag
)
from project.schema import (
    ClientType,
    ProjectType,
    TagType,
)
from project.serializers import (
    ClientSerializer,
    ProjectSerializer,
    TagSerializer
)
from utils.error_types import CustomErrorType, mutation_is_not_valid


class ClientCreateInputType(graphene.InputObjectType):
    """
    Client Create Input Type
    """

    name = graphene.String(required=True)
    address = graphene.String()
    phone_number = graphene.String()
    email = graphene.String()


class ClientUpdateInputType(graphene.InputObjectType):
    """
    Client Update Input Type
    """

    id = graphene.ID(required=True)
    phone_number = graphene.String()
    address = graphene.String()


class CreateClient(graphene.Mutation):
    class Arguments:
        data = ClientCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(ClientType)

    @staticmethod
    def mutate(root, info, data):
        serializer = ClientSerializer(data=data)
        if errors := mutation_is_not_valid(serializer):
            return CreateClient(errors=errors, ok=False)
        instance = serializer.save()
        return CreateClient(result=instance, errors=None, ok=True)


class UpdateClient(graphene.Mutation):
    class Arguments:
        data = ClientUpdateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(ClientType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = Client.objects.get(id=data['id'])
        except Client.DoesNotExist:
            return UpdateClient(errors=[
                CustomErrorType(field='nonFieldErrors',
                messages=[gettext('Client does not exist.')])
            ])
        serializer = ClientSerializer(instance=instance,
                                      data=data,
                                      partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return ClientSerializer(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateClient(result=instance, errors=None, ok=True)


class DeleteClient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(ClientType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = Client.objects.get(id=id)
        except Client.DoesNotExist:
            return DeleteClient(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=gettext('Client does not exist'))
            ])
        instance.delete()
        instance.id = id
        return DeleteClient(result=instance, errors=None, ok=True)


# Project


class ProjectCreateInputType(graphene.InputObjectType):
    """
    Project Create Input Type
    """

    title = graphene.String(required=True)
    description = graphene.String()
    client = graphene.ID(required=True)
    user_group = graphene.List(graphene.ID, required=False)


class ProjectUpdateInputType(graphene.InputObjectType):
    """
    Project Update Input Type
    """

    id = graphene.ID(required=True)
    user_group = graphene.List(graphene.ID)
    description = graphene.String()


class CreateProject(graphene.Mutation):
    class Arguments:
        data = ProjectCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(ProjectType)

    @staticmethod
    def mutate(root, info, data):
        serializer = ProjectSerializer(data=data)
        if errors := mutation_is_not_valid(serializer):
            return CreateProject(errors=errors, ok=False)
        instance = serializer.save()
        return CreateProject(result=instance, errors=None, ok=True)


class UpdateProject(graphene.Mutation):
    class Arguments:
        data = ProjectUpdateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(ProjectType)

    @staticmethod
    def mutate(root, info, data):
        # TODO : Add can  update or not
        try:
            instance = Project.objects.get(id=data['id'])
        except Project.DoesNotExist:
            return UpdateClient(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=gettext('Project Does not exist'))
            ])
        serializer = ProjectSerializer(instance=instance,
                                       data=data,
                                       context={'request': info.context},
                                       partial=True
                                    )
        if errors := mutation_is_not_valid(serializer):
            return UpdateProject(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateProject(result=instance, errors=None, ok=True)


class DeleteProject(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(ProjectType)

    @staticmethod
    def mutate(root, info, id):
        # TODO add can delete or not
        try:
            instance = Project.objects.get(id=id)
        except Project.DoesNotExist:
            return DeleteProject(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=gettext('Project does not Exist'))
            ])
        instance.delete()
        instance.id = id
        return DeleteProject(result=instance, errors=None, ok=True)


# TAG


class TagCreateInputType(graphene.InputObjectType):
    """
    TAG Create Input Type
    """
    title = graphene.String(required=True)
    description = graphene.String()
    project = graphene.ID()


class TagUpdateInputType(graphene.InputObjectType):

    """
    TAG Update Input Type
    """
    id = graphene.ID(required=True)
    description = graphene.String()
    project = graphene.ID()


class CreateTag(graphene.Mutation):
    class Arguments:
        data = TagCreateInputType(required=True)

    errors = graphene.Field(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TagType)

    @staticmethod
    def mutate(root, info, data):
        serializer = TagSerializer(data=data, 
                                     context={'request': info.context})
        if errors := mutation_is_not_valid(serializer):
            return CreateTag(errors=errors, ok=False)
        instance = serializer.save()
        return CreateTag(result=instance, errors=None, ok=True)


class UpdateTag(graphene.Mutation):
    class Arguments:
        data = TagUpdateInputType(required=True)
    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TagType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = Tag.objects.get(id=data['id'])
        except Tag.DoesNotExist:
            return UpdateTag(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=gettext('Tag does not exist'))
            ])
        serializer = TagSerializer(instance=instance, data=data,
                                    context={'request':info.context}, partial=True)
        if errors := mutation_is_not_valid(serializer):
            return UpdateTag(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateTag(result=instance, errors=None, ok=True)


class DeleteTag(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(TagType)

    @staticmethod
    def mutate(root, info, id):
        # TODO add can delete or not
        try:
            instance = Tag.objects.get(id=id)
        except Tag.DoesNotExist:
            return DeleteTag(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=gettext('Tag does not Exist'))
            ])
        instance.delete()
        instance.id = id
        return DeleteTag(result=instance, errors=None, ok=True)


class Mutation(object):
    create_client = CreateClient.Field()
    update_client = UpdateClient.Field()
    delete_client = DeleteClient.Field()
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
    create_tag = CreateTag.Field()
    update_tag = UpdateTag.Field()
    delete_tag = DeleteTag.Field()
