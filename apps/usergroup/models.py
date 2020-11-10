from django.db import models

from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User


class UserGroup(models.Model):
    """
    User group Model
    """
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(
        User, blank=True,
        through='GroupMember')

    def __str__(self):
        return self.title

    @staticmethod
    def get_for(user):
        return UserGroup.objects.filter(members=user).distinct()


class GroupMember(models.Model):
    """
    User group-Member
    """

    member = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.member)} @ {self.group.title}'

    class Meta:
        unique_together = ('member', 'group')
