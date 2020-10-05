import graphene

from apps.user import schema as user_schema, mutation as user_mutation


class Query(user_schema.Query,):
    pass


class Mutation(user_mutation.Mutation,):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
