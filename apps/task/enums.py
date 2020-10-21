import graphene

from .models import TaskGroup

StatusGrapheneEnum = graphene.Enum.from_enum(TaskGroup.STATUS)
