from collections import OrderedDict
from datetime import datetime

from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Task, TaskGroup, TimeEntry


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = '__all__'


class TimeEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeEntry
        fields = '__all__'

    def validate(self, attrs):
        errors = OrderedDict()
        errors.update(TimeEntry.clean_dates(attrs, self.instance))
        if errors:
            raise ValidationError(errors)
        return attrs
