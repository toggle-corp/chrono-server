import json

from utils.factories import (
    ClientFactory,
    UserGroupFactory,
    UserFactory,
    ProjectFactory,
    TagFactory
)
from utils.tests import ChronoGraphQLTestCase


"""
Test case for Task model mutations and query
"""


class TestCreateClient(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation CreateClient($input: ClientCreateInputType!){
            createClient(data: $input){
                errors {
                    field
                    messages
                }
                result {
                    id
                    name
                    address
                    email
                    phoneNumber
                }
                ok
            }
        }'''

        self.input = {
            "name": "GA  BUILDERS",
            "address": "kathmandu",
            "email": "gabuilders@email.com"
        }

    def test_valid_client_creation(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        print(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createClient']['ok'], content)
        self.assertIsNone(content['data']['createClient']['errors'], content)
        self.assertEqual(content['data']['createClient']['result']['name'],
                         self.input['name'])


class TestUpdateClient(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation UpdateClient($input: ClientUpdateInputType!){
            updateClient(data: $input){
                errors {
                    field
                    messages
                }
                result {
                    id
                    name
                    address
                    email
                    phoneNumber
                }
                ok
            }
        }'''

        self.input = {
            "id": ClientFactory.create().id,
            "phoneNumber": "9855052124"
        }

    def test_valid_client_updation(self):
        response = self.query(
            self.mutation,
            input_data=self.input
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['updateClient']['ok'], content)
        self.assertIsNone(content['data']['updateClient']['errors'], content)
        self.assertEqual(content['data']['updateClient']['result']['id'],
                         str(self.input['id']))


class TestDeleteClient(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation DeleteClient($id: ID!){
            deleteClient(id: $id){
                errors {
                    field
                    messages
                }
                result {
                    id
                    name
                    address
                    phoneNumber
                }
                ok
            }
        }'''
        self.client = ClientFactory.create()
        self.variables = {
            "id": self.client.id,
        }

    def test_valid_client_delete(self):
        response = self.query(
            self.mutation,
            variables=self.variables,
        )
        content = json.loads(response.content)
        self.assertTrue(content['data']['deleteClient']['ok'], content)
        self.assertIsNone(content['data']['deleteClient']['errors'], content)
        self.assertEqual(content['data']['deleteClient']['result']['name'],
                         self.client.name)
        self.assertEqual(int(content['data']['deleteClient']['result']['id']),
                         self.client.id)


"""
Test for Project mutationa and query
"""


class TestCreateProject(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation CreateProject($input: ProjectCreateInputType!){
            createProject(data: $input){
                errors {
                    field
                    messages
                }
                result {
                    id
                    title
                    client{
                        id
                    }
                    description
                    userGroup{
                        id
                    }
                }
                ok
            }
        }'''

        self.input = {
            "title": "POULTTRY MANAGEMENT SYSTEM",
            "client": ClientFactory.create().id,
            "description": "This is a management system"
        }

    def test_valid_project_creation(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        print(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createProject']['ok'], content)
        self.assertIsNone(content['data']['createProject']['errors'], content)
        self.assertEqual(content['data']['createProject']['result']['title'],
                         self.input['title'])
        self.assertEqual(int(content['data']['createProject']['result']['client']['id']),
                         self.input['client'])


class TestUpdateProject(ChronoGraphQLTestCase):
    def setUp(self):
        self.user = UserFactory.create_batch(2)
        self.client = ClientFactory.create()
        self.user_group = UserGroupFactory.create_batch(2)
        self.project = ProjectFactory.create()
        self.mutation = ''' mutation UpdateProject($input: ProjectUpdateInputType!){
            updateProject(data: $input){
                errors {
                    field
                    messages
                }
                result {
                    id
                    description
                    userGroup{
                        id
                    }
                }
                ok
            }
        }'''
        self.input = {
            "id": self.project.id,
            "userGroup": [test.id for test in self.user_group],
            "description": "This is for the test",
        }

    def test_valid_project_update(self):
        response = self.query(
            self.mutation,
            input_data=self.input
        )
        content = json.loads(response.content)
        print(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['updateProject']['ok'], content)


class TestDeleteProject(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation DeleteProject($id: ID!){
                deleteProject(id: $id){
                    errors {
                        field
                        messages
                    }
                    result {
                        id
                        title
                    }
                    ok
                }
            }'''
        self.project = ProjectFactory.create()
        self.variables = {
            "id": self.project.id,
        }

    def test_valid_project_delete(self):
        response = self.query(
            self.mutation,
            variables=self.variables,
        )
        content = json.loads(response.content)
        self.assertTrue(content['data']['deleteProject']['ok'], content)
        self.assertIsNone(content['data']['deleteProject']['errors'], content)
        self.assertEqual(content['data']['deleteProject']['result']['title'],
                         self.project.title)
        self.assertEqual(int(content['data']['deleteProject']['result']['id']),
                         self.project.id)


## Test for Tag mutation and query


class TestCreateTag(ChronoGraphQLTestCase):
    def setUp(self):
        self.user = UserFactory.create_batch(2)
        self.client = ClientFactory.create()
        self.user_group = UserGroupFactory.create_batch(2,
            members=self.user
        )
        self.project = ProjectFactory.create(
            user_group=self.user_group
        )
        self.mutation = '''mutation CreateTag($input: TagCreateInputType!){
            createTag(data: $input){
                errors {
                    field
                    messages
                }
                result {
                    title
                    description
                    project{
                        id
                    }
                }
                ok
            }
        }'''

        self.input = {
            "title": "Test for the tag creation",
            "description": "This is the description of the tag",
            "project": self.project.id,
        }

    def test_valid_tag_creation(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createTag']['ok'], content)
        self.assertIsNone(content['data']['createTag']['errors'], content)
        self.assertEqual(content['data']['createTag']['result']['title'],
                         self.input['title'])


class TestUpdateTag(ChronoGraphQLTestCase):
    def setUp(self):
        self.tag = TagFactory.create()
        self.project = ProjectFactory.create()
        self.mutation = ''' mutation UpdateTag($input: TagUpdateInputType!){
            updateTag(data: $input){
                errors {
                    field
                    messages
                }
                result {
                    id
                    title
                    project{
                        id
                    }
                    description
                }
                ok
            }
        }'''
        self.input = {
            "id": self.tag.id,
            "description": "This is for the test",
            "project": self.project.id
        }

    def test_valid_tag_update(self):
        response = self.query(
            self.mutation,
            input_data=self.input
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['updateTag']['ok'], content)


class TestDeleteTag(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation DeleteTag($id: ID!){
                deleteTag(id: $id){
                    errors {
                        field
                        messages
                    }
                    result {
                        id
                        title
                    }
                    ok
                }
            }'''
        self.tag = TagFactory.create()
        self.variables = {
            "id": self.tag.id,
        }

    def test_valid_tag_delete(self):
        response = self.query(
            self.mutation,
            variables=self.variables,
        )
        content = json.loads(response.content)
        print(response.content)
        self.assertTrue(content['data']['deleteTag']['ok'], content)
        self.assertIsNone(content['data']['deleteTag']['errors'], content)
        self.assertEqual(content['data']['deleteTag']['result']['title'],
                         self.tag.title)
        self.assertEqual(int(content['data']['deleteTag']['result']['id']),
                         self.tag.id)
