from django.db import models
from django.core.exceptions import ValidationError
from django_enumfield import enum
from django.utils.translation import gettext_lazy as _


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
    # need to create Tag model
    #tags = model.ManyToManyField(Tag, blank=True)

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

    def clean(self):
        # TODO : Check for the overlap
        if self.end_time and self.start_time > self.end_time:
            raise ValidationError('Start time should be less than End time')

        time_check = models.Q(
            start_time__lt=self.start_time,
            end_time__gt=self.start_time
        )
        # if provided end_time 
        if self.end_time:
            time_check |= models.Q(
                start_time__lt=self.end_time,
                end_time__gt=self.end_time
            )

        if TimeEntry.objects.exclude(pk=self.pk).filter(
            time_check,
            user=self.user,
            task__task_group=self.task.task_group,
            date=self.date,
            ).exists():
            raise ValidationError("Time  Entry overlap for another in this day")

    def total_time(self):
        return (
            datetime.combine(datetime.now(), self.end_time) -
            datetime.combine(datetime.now(), self.start_time)
        )

    def total_time_in_sec(self):
        return self.total_time().total_seconds()

    @property
    def duration(self):
        end_datetime = datetime.combine(self.date, self.end_time)
        start_datetime = datetime.combine(self.date, self.start_time)
        difference = end_datetime - start_datetime
        secs = round(difference.total_seconds(), 0)
        return round(secs / 3600.0, 2)

