import graphene
from graphene import Field
from graphene_django_extras import DjangoObjectField, DjangoObjectType 

from user.models import Profile
from user.enums import GenderGrapheneEnum


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = []
    gender = graphene.Field(GenderGrapheneEnum)

class Query:
    profile = DjangoObjectField(ProfileType)
