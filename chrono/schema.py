import graphene

from user import schema as user_schema, mutations as user_mutations
from usergroup import schema as usergroup_schema, mutations as usergroup_mutations
from task import schema as task_schema, mutations as task_mutations


class Query(graphene.ObjectType,
            user_schema.Query,
            usergroup_schema.Query,
            task_schema.Query,):
    pass


class Mutation(graphene.ObjectType,
               user_mutations.Mutation,
               usergroup_mutations.Mutation,
               task_mutations.Mutation,):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
