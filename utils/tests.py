import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene_django.utils import GraphQLTestCase

User = get_user_model()


class ChronoGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_URL = '/graphql'
    GRAPHQL_SCHEMA = 'chrono.schema.schema'

    def create_user(self):
        user_password = 'test123'
        user = User.objects.create_user(
            username='jon@dave.com',
            email='jon@dave.com',
            password=user_password,
        )
        user.user_password = user_password
        return user 