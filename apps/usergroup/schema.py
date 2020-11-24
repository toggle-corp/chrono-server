import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, DjangoObjectType

from usergroup.models import UserGroup, GroupMember


class UserGroupType(DjangoObjectType):
    class Meta:
        model = UserGroup
        fields = '__all__'

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class GroupMemberType(DjangoObjectType):
    class Meta:
        model = GroupMember
        fields = '__all__'


class Query(object):
    group = graphene.Field(UserGroupType)
    groupslist = graphene.List(GroupMemberType,)
    groups = graphene.Field(GroupMemberType, id=graphene.Int())
    groupmember = graphene.Field(GroupMemberType)

    def resolve_groupslist(self, info, **kwargs):
        return GroupMember.objects.all()

    def resolve_groups(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return GroupMember.objects.get(pk=id)
        return None
