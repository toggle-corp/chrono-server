from django.utils.translation import gettext
from django.contrib.auth import login, logout
import graphene
from graphene_file_upload.scalars import Upload
from graphene_django.rest_framework.mutation import SerializerMutation

from user.models import User
from user.schema import  UserType
from user.serializers import (
    ProfileSerializer,
    LoginSerializer,
    RegisterSerializer
)
from user.enums import GenderGrapheneEnum
from utils.error_types import CustomErrorType, mutation_is_not_valid


class RegisterMutation(SerializerMutation):
    class Meta:
        serializer_class = RegisterSerializer


class LoginMutation(SerializerMutation):
    class Meta:
        serializer_class = LoginSerializer

    me = graphene.Field(UserType)

    @classmethod
    def perform_mutate(cls, serializer, info):
        if user := serializer.validated_data.get('user', None):
            login(info.context, user)
        return cls(errors=None, me=user)


class LogoutMutation(graphene.Mutation):
    ok = graphene.Boolean()

    def mutate(self, info, *args, **kwargs):
        if info.context.user.is_authenticated:
            logout(info.context)
        return LogoutMutation(ok=True)


class UserCreateInputType(graphene.InputObjectType):
    """
    Profile Create InputType
    """
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    username = graphene.String(required=True)
    display_picture = Upload(required=False)
    phone_number = graphene.String()
    address = graphene.String()
    gender = graphene.Field(GenderGrapheneEnum)
    join_date = graphene.Date()
    date_of_birth = graphene.Date()
    position = graphene.String()
    signature = Upload(required=False)


class UserUpdateInputType(graphene.InputObjectType):
    """
    Profile Update InputType
    """
    id = graphene.ID(required=True)
    phone_number = graphene.String()
    address = graphene.String()
    position = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        user = UserCreateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user):
        serializer = ProfileSerializer(data=user)
        if errors := mutation_is_not_valid(serializer):
            return CreateUser(errors=errors, ok=False)
        instance = serializer.save()
        return CreateUser(user=instance, errors=None, ok=True)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user = UserUpdateInputType(required=True)

    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user):
        try:
            instance = User.objects.get(id=user['id'])
        except User.DoesNotExist:
            return UpdateUser(errors=[
                CustomErrorType(field='non_field_errors',
                messages=[gettext('User does not exist.')])
            ])
        serializer = ProfileSerializer(instance=instance,
                                       data=user,
                                       partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return UpdateUser(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateUser(user=instance, errors=None, ok=True)


class Mutation(object):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    login = LoginMutation.Field()
    register = RegisterMutation.Field()
    logout = LogoutMutation.Field()
