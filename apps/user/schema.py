from graphene_django import DjangoObjectType
from graphene import Field, List

from .models import Profile


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = []


class Query:
    profile = DjangoObjectField(ProfileType)
