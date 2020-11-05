from django.utils.translation import gettext
from rest_framework import serializers

from project.models import Client, Project, Tag
<<<<<<< HEAD
from usergroup.models import UserGroup
=======
>>>>>>> Model and schema setup


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

<<<<<<< HEAD
=======
    def validate_user_group(self, group):
        if not group.can_get(self.context['request'].user):
            raise serializers.ValidationError(gettext('Invalid user group'))
        return group

>>>>>>> Model and schema setup

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
