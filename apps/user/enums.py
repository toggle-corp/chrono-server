import graphene

from user.models import User

GenderGrapheneEnum = graphene.Enum.from_enum(User.GENDER)
