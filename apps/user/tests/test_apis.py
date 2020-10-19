import json

from django.contrib.auth import get_user_model
from utils.tests import ChronoGraphQLTestCase
from utils.factories import UserFactory

User = get_user_model()


class TestLogin(ChronoGraphQLTestCase):
    def setUp(self) -> None:
        self.user = self.create_user()
        self.login_query = '''
            mutation MyMutation ($email: String!, $password: String!){
                login(input: {email: $email, password: $password}) {
                    errors {
                        field
                        messages
                    }
                    me {
                        email
                    }
                }
            }
        '''
        self.me_query = '''
            query MeQuery {
                me {
                    email
                }
            }
        '''

    def test_valid_login(self):
        response = self.query(
            self.login_query,
            variables={'email': self.user.email, 'password': self.user.user_password}
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertIsNone(content['data']['login']['errors'])
        self.assertIsNotNone(content['data']['login']['me'])
        self.assertIsNotNone(content['data']['login']['me']['email'])

        response = self.query(
            self.me_query,
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['me']['email'], self.user.email)

    def test_invalid_email(self):
        response = self.query(
            self.login_query,
            variables={'email': 'abc@mail.com', 'password': self.user.user_password},
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertIn('non_field_errors', [each['field'] for each in content['data']['login']['errors']])
        self.assertIsNone(content['data']['login']['me'])


class TestRegister(ChronoGraphQLTestCase):
    def setUp(self):
        self.register = '''
            mutation Register ($input: RegisterMutationInput!){
                register(input: $input) {
                    errors {
                        field
                        messages
                    }
                }
            }
        '''
        self.input = {
            'email': 'jon@dave.com',
            'username': 'jon@dave.com',
            'password': 'test123',
        }

    def test_valid_registration(self):
        response = self.query(
            self.register,
            input_data=self.input,
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertIsNone(content['data']['register']['errors'])


class TestLogOut(ChronoGraphQLTestCase):
    def setUp(self) -> None:
        self.user = self.create_user()
        self.login_query = '''
            mutation MyMutation ($email:String!, $password: String!){
                login(input: {email: $email, password: $password}){
                    errors {
                        field
                        messages
                    }
                }
            }
        '''
        self.me_query = '''
            query MeQuery{
                me{
                    email
                }

            }
        '''
        self.logout_query = '''
            mutation LogOut {
                logout{
                    ok
                }
            }
        '''

    def test_valid_logout(self):
        response = self.query(
            self.login_query,
            variables={'email':self.user.email, 'password':self.user.user_password},
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertIsNone(content['data']['login']['errors'])

        response = self.query(
            self.me_query,
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['me']['email'], self.user.email)

        response = self.query(
            self.logout_query,
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        response = self.query(
            self.me_query
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['me'], None)


class TestUserCreate(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''
            mutation CreateUser($input: UserCreateInputType!){
                createUser(user: $input){
                    errors{
                        field
                        messages
                    }
                    user {
                        id
                        username
                        phoneNumber
                    }
                    ok
                }
            }
        '''

        self.input = {
            'username': 'test@gmail.com',
            'email': 'test@gmail.com',
            'password': 'nepal1111',
            'phoneNumber': '6171818111',

        }

    def test_valid_profile_creation(self) -> None:
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createUser']['ok'], content)
        self.assertIsNone(content['data']['createUser']['errors'], content)
        self.assertEqual(content['data']['createUser']['user']['username'],
                         self.input['username'])
        self.assertEqual(content['data']['createUser']['user']['phoneNumber'],
                         self.input['phoneNumber'])


class TestUpdateProfile(ChronoGraphQLTestCase):
    def setUp(self):
        self.user = self.create_user()
        self.mutation_update = '''
            mutation UpdateUser($input: UserUpdateInputType!){
                updateUser(user: $input){
                    errors{
                        field
                        messages
                    }
                    user{
                        id
                        phoneNumber
                        address
                        position
                    }
                    ok
                }
            }
        '''
        self.input = {
            "id": self.user.id,
            "position": "Developer",
            "address": "Kathmandu",
            "phoneNumber": "9823456789",
        }

    def test_valid_profile_update(self) -> None:
        response = self.query(
            self.mutation_update,
            input_data=self.input,
        )
        content = json.loads(response.content)
        print("data", content)
        self.assertResponseNoErrors(content)
        self.assertTrue(content['data']['updateUser']['ok'], content)
        self.assertIsNone(content['data']['updateUser']['errors'], content)
        self.assertEqual(content['data']['updateUser']['user']['position'],
                         self.input['position'])
