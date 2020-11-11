from django.contrib.auth import get_user_model
import graphene
from graphene_django_extras import DjangoObjectField, DjangoObjectType

from user.models import User
from user.enums import GenderGrapheneEnum


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = (
            'is_staff',
            'is_superuser',
            'is_active',
            'groups',
            'user_permissions',
            'password',
        )

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class Query(object):
    profile = graphene.Field(UserType)
    me = graphene.Field(UserType)

    def resolve_me(parent, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
