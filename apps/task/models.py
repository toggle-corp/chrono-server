from collections import OrderedDict

from django.db import models
from django.core.exceptions import ValidationError
from django_enumfield import enum
from django.utils.translation import gettext_lazy as _, gettext


from user.models import User
from usergroup.models import UserGroup

from utils.models import BaseModel


class TaskGroup(BaseModel):

    class STATUS(enum.Enum):
        DONE = 0
        NOTDONE = 1
        INPROGRESS = 2

        __labels__ = {
            DONE: _("Done"),
            NOTDONE: _("Not-Done"),
            INPROGRESS: _("In-Progress"),
        }

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = enum.EnumField(STATUS, null=True)
    users = models.ManyToManyField(User, blank=True,)
    user_group = models.ManyToManyField(UserGroup, blank=True,)

    def __str__(self):
        return self.title

    @staticmethod
    def get_for(user):
        return TaskGroup.objects.filter(
            user_group__members=user
        ).distinct()


class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    external_url = models.URLField(max_length=255,
                                   blank=True, null=True)
    task_group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE,
                                    blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)

    def __str__(self):
        return self.title


class TimeEntry(models.Model):
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(default=None, blank=True,
                                null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.task.title} by {str(self.user)} {str(self.start_time)}'

    @staticmethod
    def clean_dates(values, instance=None):
        errors = OrderedDict()
        start_time = values.get('start_time', getattr(instance, 'start_time', None))
        end_time = values.get('end_time', getattr(instance, 'end_time', None))
        date = values.get('date', getattr(instance, 'date', None))
        user = values.get('user',getattr(instance, 'date', None))
        if end_time and start_time > end_time:
            errors['end_time'] = gettext('start_time must be less than end_time')

        time_check = models.Q(
            start_time__lt=start_time,
            end_time__gt=start_time
        )
        # provided the end_time
        if end_time:
            time_check |= models.Q(
                start_time__lt=end_time,
                end_time__gt=end_time
            )
        if TimeEntry.objects.filter(
                time_check,
                date=date,
                user=user,
                ).exists():
            errors['date'] = gettext('This time slot overlaps with another '
                                  'for this day')

        return errors

    @property
    def duration(self):
        if not end_time:
            return 0
        end_datetime = datetime.combine(self.date, self.end_time)
        start_datetime = datetime.combine(self.date, self.start_time)
        difference = end_datetime - start_datetime
        secs = round(difference.total_seconds(), 0)
        return round(secs / 3600.0, 2)
