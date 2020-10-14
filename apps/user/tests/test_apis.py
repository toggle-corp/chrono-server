import json

from django.contrib.auth import get_user_model
from utils.tests import ChronoGraphQLTestCase
from utils.factories import ProfileFactory, UserFactory

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


class TestProfileCreate(ChronoGraphQLTestCase):
    def setUp(self):
        self.user = self.create_user()
        self.mutation = '''
            mutation CreateProfile($input: ProfileCreateInputType!){
                createProfile(profile: $input){
                    errors{
                        field
                        messages
                    }
                    profile {
                        user{
                            id
                        }
                        phoneNumber
                        gender
                    }
                    ok
                }
            }
        '''
        
        self.input = {
            'user':UserFactory().id,
            'phoneNumber':"85222153330",
            'address':"Kathmandu",
            'gender':"MALE"

        }

    def test_valid_profile_creation(self) -> None:
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createProfile']['ok'], content)
        self.assertIsNone(content['data']['createProfile']['errors'], content)
        self.assertEqual(content['data']['createProfile']['profile']['phoneNumber'],
                        self.input['phoneNumber'])
        self.assertEqual(int(content['data']['createProfile']['profile']['user']['id']),
                        self.input['user'])
        self.assertEqual(content['data']['createProfile']['profile']['gender'],
                        self.input['gender'])


class TestUpdateProfile(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation_create = '''
            mutation CreateProfile($input: ProfileCreateInputType!){
                createProfile(profile: $input){
                    errors{
                        field
                        messages
                    }
                    profile {
                        user{
                            id
                        }
                        phoneNumber
                        gender
                    }
                    ok
                }
            }
        '''
        
        self.input_create = {
            'user':UserFactory().id,
            'phoneNumber':"85222153330",
            'address':"Kathmandu",
            'gender':"MALE"

        }
        response = self.query(
            self.mutation_create,
            input_data=self.input_create,
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createProfile']['ok'], content)

        self.mutation_update = '''
            mutation UpdateProfile($input: ProfileUpdateInputType!){
                updateProfile(event: $input){
                    errors{
                        field
                        messages
                    }
                    profile{
                        id
                        user{
                            username
                        }
                        phone_number
                        address
                        position
                    }
                }
            }
        '''
        self.input_update = {
            "id":ProfileFactory.create().id,
            "position":"Developer",
            "user":self.input_create['id'],
        }

    def test_valid_profile_update(self):
        response = self.query(
            self.mutation_update,
            input_data=self.input_update,
        )
        content = json.loads(response.content)
            
        self.assertResponseNoErrors(content)
        self.assertTrue(content['data']['updateProfile']['ok'], content)
        self.assertIsNone(content['data']['updateProfile']['errors'], content)
        self.assertEqual(content['data']['updateProfile']['profile']['id'],
                        self.input['id'])
        self.assertEqual(content['data']['updateProfile']['profile']['position'],
                        self.input['position'])
            