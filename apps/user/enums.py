import graphene

from user.models import Profile

GenderGrapheneEnum = graphene.Enum.from_enum(Profile.GENDER)