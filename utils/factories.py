import factory
from factory.django import DjangoModelFactory

from user.models import Profile


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'user.User'
    
    email = factory.Sequence(lambda n: f'test{n}@email.com')
    username = factory.Sequence(lambda n: f'usename{n}')


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = 'user.Profile'
    
    user = factory.SubFactory(UserFactory)
    