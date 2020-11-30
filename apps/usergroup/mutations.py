from django.utils.translation import gettext
import graphene
from graphene_file_upload.scalars import Upload

from usergroup.models import UserGroup, GroupMember
from usergroup.schema import UserGroupType, GroupMemberType
from usergroup.serializers import UserGroupSerializer, GroupMemberSerializer
from utils.error_types import CustomErrorType, mutation_is_not_valid


class UserGroupCreateInputType(graphene.InputObjectType):
    """
    User-Group Create Input Type
    """

    title = graphene.String(required=True)
    description = graphene.String()


class UserGroupUpdateInputType(graphene.InputObjectType):
    """
    User-Group Update Input Type
    """

    id = graphene.ID(required=True)
    description = graphene.String()


class GroupMemberCreateInputType(graphene.InputObjectType):
    """
    memebers for the group
    """
    member = graphene.ID()
    group = graphene.ID()


class CreateUserGroup(graphene.Mutation):
    class Arguments:
        data = UserGroupCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(UserGroupType)

    @staticmethod
    def mutate(root, info, data):
        serializer = UserGroupSerializer(data=data)
        if errors := mutation_is_not_valid(serializer):
            return CreateUserGroup(errors=errors, ok=False)
        instance = serializer.save()
        return CreateUserGroup(result=instance, errors=None, ok=True)


class UpdateUserGroup(graphene.Mutation):
    class Arguments:
        data = UserGroupUpdateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(UserGroupType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = UserGroup.objects.get(id=data['id'])
        except UserGroup.DoesNotExist:
            return UpdateUserGroup(errors=[
                CustomErrorType(field='nonFieldErrors',
                messages=[gettext('UserGroup does not exist.')])
            ])
        serializer = UserGroupSerializer(instance=instance,
                                         data=data,
                                         partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return UpdateUserGroup(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateUserGroup(result=instance, errors=None, ok=True)


class CreateGroupMember(graphene.Mutation):
    class Arguments:
        data = GroupMemberCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(GroupMemberType)

    @staticmethod
    def mutate(root, info, data):
        serializer = GroupMemberSerializer(data=data)
        if errors := mutation_is_not_valid(serializer):
            return CreateGroupMember(errors=errors, ok=False)
        instance = serializer.save()
        return CreateGroupMember(result=instance, errors=None, ok=True)


class DeleteGroupMember(graphene.Mutation):
    """
    Delete memebers from the group members
    """
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    result = graphene.Field(GroupMemberType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = GroupMember.objects.get(id=id)
        except GroupMember.DoesNotExist:
            return DeleteGroupMember(errors=[
                CustomErrorType(field='nonFieldErrors',
                                messages=gettext('Member does not exist.'))
            ])
        instance.delete()
        instance.id = id
        return DeleteGroupMember(result=instance, errors=None, ok=True)


class Mutation(object):
    create_usergroup = CreateUserGroup.Field()
    update_usergroup = UpdateUserGroup.Field()
    create_groupmember = CreateGroupMember.Field()
    delete_groupmember = DeleteGroupMember.Field()
