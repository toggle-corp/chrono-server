from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, DjangoObjectType 

from user.models import Profile, User
from user.enums import GenderGrapheneEnum

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = []
    gender = graphene.Field(GenderGrapheneEnum)

class Query(object):
    profile = DjangoObjectField(ProfileType)
    me = graphene.Field(UserType)

    def resolve_me(parent, info):
        if info.context.user.is_authenticated:
            return info.context.user 
        return None
        