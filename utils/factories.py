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

    members = factory.SubFactory(UserFactory)

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for member in extracted:
                self.members.add(member)


class GroupMemeberFactory(DjangoModelFactory):
    class Meta:
        model = 'usergroup.GroupMember'

    member = factory.SubFactory(UserFactory)
    group = factory.SubFactory(UserGroupFactory)


class TaskGroupFactory(DjangoModelFactory):
    class Meta:
        model = 'task.TaskGroup'

    start_date = factory.Faker('date')
    end_date = factory.Faker('date')
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    users = factory.SubFactory(UserFactory)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.users.add(user)


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


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = 'project.Client'


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = 'project.Project'

    title = factory.Faker('name')
    client = factory.SubFactory(ClientFactory)
    user_group = factory.SubFactory(UserGroupFactory)

    @factory.post_generation
    def user_group(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.user_group.add(group)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = 'project.Tag'

    project = factory.SubFactory(ProjectFactory)
