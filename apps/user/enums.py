import graphene

from .modles import Profile

GenderGrapheneEnum = graphene.Enum.from_enum(Contact.GENDER)