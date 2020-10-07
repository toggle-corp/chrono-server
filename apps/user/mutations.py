from django.utils.translation import gettext
from django.contrib.auth import login, logout
import graphene
from graphene_file_upload.scalars import Upload
from graphene_django.rest_framework.mutation import SerializerMutation

from user.models import Profile 
from user.schema import ProfileType, UserType
from user.serializers import ProfileSerializer, LoginSerializer, RegisterSerializer
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


class ProfileCreateInputType(graphene.InputObjectType):
    """
    Profile Create InputType
    """
    user = graphene.ID(required=True)
    display_picture = Upload(required=False)
    phone_number = graphene.String(required=True)
    address = graphene.String()
    gender = graphene.Field(GenderGrapheneEnum)
    join_date = graphene.Date()
    date_of_birth = graphene.Date()
    position = graphene.String()
    signature = Upload(required=False)


class ProfileUpdateInputType(graphene.InputObjectType):
    """
    Profile Update InputType
    """
    id = graphene.ID(required=True)
    user = graphene.ID()
    phone_number = graphene.String()
    address = graphene.String()
    position = graphene.String()


class CreateProfileMutation(graphene.Mutation):
    class Arguments:
        profile = ProfileCreateInputType(required=True)
    
    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    profile = graphene.Field(ProfileType)

    @staticmethod
    def mutate(root, info, profile):
        serializer = ProfileSerializer(data=profile)
        if errors := mutation_is_not_valid(serializer):
            return CreateProfileMutation(errors=errors, ok=False)
        instance = serializer.save()
        return CreateProfileMutation(profile=instance, errors=None, ok=True)


class UpdateProfileMutation(graphene.Mutation):
    class Arguments:
        profile = ProfileUpdateInputType(required=True)
    
    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    profile = graphene.Field(ProfileType)

    @staticmethod
    def mutate(root, info, profile):
        try:
            instance = Profile.objects.get(id=profile['id'])
        except Profile.DoesNotExist:
            return UpdateProfileMutation(errors=[
                CustomErrorType(field='non_field_errors', 
                messages=[gettext('Profile does not exist.')])
            ])
        serializer = ProfileSerializer(instance=instance,
                                      data=profile,
                                      partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return UpdateProfileMutation(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateProfileMutation(profile=instance, errors=None, ok=True)


class Mutation(object):
    create_profile = CreateProfileMutation.Field()
    update_profile =  UpdateProfileMutation.Field()
    login = LoginMutation.Field()
    register = RegisterMutation.Field()
    logout = LogoutMutation.Field()
