from django.db import models

from utils.models import BaseModel

from usergroup.models import UserGroup


class Client(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Project(BaseModel):
    """
    Project Model
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user_group = models.ManyToManyField(UserGroup, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               blank=True, null=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_for(user):
        """
        Project accessible if user is
        member of the group
        """
        return Project.objects.filter(
            user_group__members=user
        ).distinct()


class Tag(BaseModel):
    """
    Tag mdoel
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                blank=True, null=True)

    class Meta:
        unique_together = (('title', 'project'), )

    def __str__(self):
        return f'{self.project.title} {self.title}'

    @staticmethod
    def get_for(user):
        """
        Tag can be accessed only if
        user is member of group in the project tag
        """
        projects = Project.get_for(user)
        return Tag.objects.filter(
            projects__in=[projects]
        )
