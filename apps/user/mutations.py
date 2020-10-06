import graphene
from graphene_file_upload.scalars import Upload
from django.utils.translation import gettext_lazy as _

from user.models import Profile 
from user.schema import ProfileType
from user.serializers import ProfileSerializer
from user.enums import GenderGrapheneEnum
from utils.error_types import CustomErrorType, mutation_is_not_valid


class ProfileCreateInputType(graphene.InputObjectType):
    """
    Profile Create InputType
    """
    user = graphene.ID(required=True)
    middle_name = graphene.String()
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
    user = graphene.ID(required=True)
    phone_number = graphene.String()
    address = graphene.String()
    position = graphene.String()


class CreateProfile(graphene.Mutation):
    class Arguments:
        profile = ProfileCreateInputType(required=True)
    
    errors = graphene.List(CustomErrorType)
    ok = graphene.Boolean()
    profile = graphene.Field(ProfileType)

    @staticmethod
    def mutate(root, info, profile):
        serializer = ProfileSerializer(data=profile)
        if errors := mutation_is_not_valid(serializer):
            return CreateProfile(errors=errors, ok=False)
        instance = serializer.save()
        return CreateProfile(profile=instance, errors=None, ok=True)


class UpdateProfile(graphene.Mutation):
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
            return UpdateProfile(errors=[
                CustomErrorType(field='non_field_errors', 
                messages=[_('Profile does not exist.')])
            ])
        serializer = ProfileSerializer(instance=instance,
                                      data=profile,
                                      partial=True)
        if errors:= mutation_is_not_valid(serializer):
            return UpdateProfile(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateProfile(profile=instance, errors=None, ok=True)


class Mutation(object):
    create_profile = CreateProfile.Field()
    update_profile =  UpdateProfile.Field()
