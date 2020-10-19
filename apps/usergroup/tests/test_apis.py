import json

from utils.tests import ChronoGraphQLTestCase
from utils.factories import UserFactory, UserGroupFactory


class TestCreateUserGoup(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation CreateUserGroup($input: UserGroupCreateInputType!){
            createUsergroup(group: $input){
                errors {
                    field
                    messages
                }
                group {
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
        print("data", content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createUsergroup']['ok'], content)
        self.assertIsNone(content['data']['createUsergroup']['errors'], content)
        self.assertEqual(content['data']['createUsergroup']['group']['title'],
                         self.input['title'])


class TestUpdateUserGoup(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation UpdateUserGroup($input: UserGroupUpdateInputType!){
            updateUsergroup(group: $input){
                errors {
                    field
                    messages
                }
                group {
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
        print("data", content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['updateUsergroup']['ok'], content)
        self.assertIsNone(content['data']['updateUsergroup']['errors'], content)
        self.assertEqual(content['data']['updateUsergroup']['group']['description'],
                         self.input['description'])


class TestCreateGroupMember(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation CreateGroupMember($input: GroupMemberCreateInputType!){
            createGroupmember(groupmember: $input){
                errors {
                    field
                    messages
                }
                groupmember {
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
        print("data", content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createGroupmember']['ok'], content)
        self.assertIsNone(content['data']['createGroupmember']['errors'], content)
        self.assertEqual(content['data']['createGroupmember']['groupmember']['member']['id'],
                         str(self.input['member']))
        self.assertEqual(content['data']['createGroupmember']['groupmember']['group']['id'],
                         str(self.input['group']))


class DeleteGroupMember(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = ''' mutation  DeleteGroupMember($group: ID!, $member: ID!){
            deleteGroupmember(group: $group, member: $member){
                errors {
                    field
                    messages
                }
                ok
                groupmember{
                    member{
                        id
                        username
                        email
                    }
                }
            }
        }'''
        self.variables = {
            "member": UserFactory.create().id,
            "group": UserGroupFactory.create().id,
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
        self.assertIsNotNone(content['data']['deleteGroupmember']['groupmember']['member']['id'])
