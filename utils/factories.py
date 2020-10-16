import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'user.User'

    email = factory.Sequence(lambda n: f'test{n}@email.com')
    username = factory.Sequence(lambda n: f'usename{n}')
