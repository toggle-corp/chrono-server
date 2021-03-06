import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import (
    DjangoObjectField,
    DjangoObjectType,
    DjangoFilterListField,
)
from project.models import Client, Project, Tag
from project.filters import ProjectFilter


class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        fields = '__all__'


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectListType(DjangoObjectType):
    class Meta:
        model = Project
        filterset_class = ProjectFilter


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = '__all__'


class Query(object):
    client = DjangoObjectField(ClientType)
    project = DjangoObjectField(ProjectType)
    project_list = DjangoFilterListField(ProjectListType)
    tag = DjangoObjectField(TagType)
