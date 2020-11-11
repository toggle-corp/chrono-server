import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'user.User'

    email = factory.Sequence(lambda n: f'test{n}@email.com')
    username = factory.Sequence(lambda n: f'usename{n}')


class UserGroupFactory(DjangoModelFactory):
    class Meta:
        model = 'usergroup.UserGroup'


class TaskGroupFactory(DjangoModelFactory):
    class Meta:
        model = 'task.TaskGroup'

    start_date = factory.Faker('date')
    end_date = factory.Faker('date')
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = 'task.Task'

    user = factory.SubFactory(UserFactory)
    task_group = factory.SubFactory(TaskGroupFactory)
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class TimeEntryFactory(DjangoModelFactory):
    class Meta:
        model = 'task.TimeEntry'

    user = factory.SubFactory(UserFactory)
    task = factory.SubFactory(TaskFactory)
    start_time = factory.Faker('time')
    date = factory.Faker('date')
