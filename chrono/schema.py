import graphene

from user import schema as user_schema, mutations as user_mutations


class Query(graphene.ObjectType, user_schema.Query,):
    pass



class Mutation(graphene.ObjectType,user_mutations.Mutation,):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
