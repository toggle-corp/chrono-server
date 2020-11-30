import json

from utils.tests import ChronoGraphQLTestCase
from utils.factories import (
    UserFactory,
    UserGroupFactory,
    GroupMemeberFactory
)


class TestCreateUserGoup(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation CreateUserGroup($input: UserGroupCreateInputType!){
            createUsergroup(data: $input){
                errors {
                    field
                    messages
                }
                result {
                    id
                    title
                    description
                }
                ok
            }
        }'''

        self.input = {
            "title": "BACKEND",
            "description": "Group of backend developers",
        }

    def test_valid_usergroup_creation(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createUsergroup']['ok'], content)
        self.assertIsNone(content['data']['createUsergroup']['errors'], content)
        self.assertEqual(content['data']['createUsergroup']['result']['title'],
                         self.input['title'])


class TestUpdateUserGoup(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation UpdateUserGroup($input: UserGroupUpdateInputType!){
            updateUsergroup(data: $input){
                errors {
                    field
                    messages
                }
                result {
                    id
                    title
                    description
                }
                ok
            }
        }'''

        self.input = {
            "id": UserGroupFactory.create().id,
            "description": "Group of backend developers!!!!!!!!!",
        }

    def test_valid_usergroup_update(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['updateUsergroup']['ok'], content)
        self.assertIsNone(content['data']['updateUsergroup']['errors'], content)
        self.assertEqual(content['data']['updateUsergroup']['result']['description'],
                         self.input['description'])


class TestCreateGroupMember(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation CreateGroupMember($input: GroupMemberCreateInputType!){
            createGroupmember(data: $input){
                errors {
                    field
                    messages
                }
                result {
                    id
                    member{
                        id
                        username

                    }
                    group{
                        id
                        title
                    }
                }
                ok
            }
        }'''

        self.input = {
            "member": UserFactory.create().id,
            "group": UserGroupFactory.create().id,
        }

    def test_valid_usergroup_creation(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createGroupmember']['ok'], content)
        self.assertIsNone(content['data']['createGroupmember']['errors'], content)
        self.assertEqual(content['data']['createGroupmember']['result']['member']['id'],
                         str(self.input['member']))
        self.assertEqual(content['data']['createGroupmember']['result']['group']['id'],
                         str(self.input['group']))


class DeleteGroupMember(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = ''' mutation  DeleteGroupMember($id: ID!){
            deleteGroupmember(id: $id){
                errors {
                    field
                    messages
                }
                ok
                result{
                    member{
                        id
                        username
                        email
                    }
                }
            }
        }'''
        self.variables = {
            "id": GroupMemeberFactory.create().id,
        }

    def test_valid_groupmember_delete(self):
        response = self.query(
            self.mutation,
            variables=self.variables,
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['deleteGroupmember']['ok'], content)
        self.assertIsNone(content['data']['deleteGroupmember']['errors'], content)
        self.assertIsNotNone(content['data']['deleteGroupmember']['result']['member']['id'])
