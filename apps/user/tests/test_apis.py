import json

from utils.tests import ChronoGraphQLTestCase
from utils.factories import ProfileFactory, UserFactory


class TestLogin(ChronoGraphQLTestCase):
    def setUp(self):
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
    def setUp(self):
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
                variables={'email':self.user.email, 'password':self.user.user_password}
            )
            content = json.loads(response.content)

            self.assertResponseNoErrors(content)
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
        self.mutation = '''
            mutation CreateProfile($input: ProfileCreateInputType!){
                createProfile(profile: $input){
                    errors{
                        field
                        messages
                    }
                    profile {
                        user{
                            name
                        }
                        display_picture
                        phone_number
                        gender
                        join_date
                        date_of_birth
                        position
                        signature
                    }
                    ok
                }
            }'''
        
        self.input = {
            'user':UserFactory().id,
            'phone_number':"85222153330",
            'gender': MALE,

        }

        def test_valid_profile_creation(self):
            response = self.query(
                self.mutation,
                input_data=self.input,
            )

            content = json.loads(response.content)

            self.assertResponseNoErrors(content)
            self.assertTrue(content['data']['CreateProfile']['ok'], content)
            self.assertIsNone(content['data']['CreateProfile']['errors'], content)
            self.assertEqual(content['data']['CreateProfile']['profile']['phone_number'],
                            self.input['phone_number'])
            self.assertEqual(content['data']['CreateProfile']['profile']['user'],
                            self.input['user'])


class TestUpdateProfile(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''
            mutation UpdateProfile($input: ProfileUpdateInputType!){
                updateProfile(event: $input){
                    errors{
                        field
                        messages
                    }
                    profile{
                        id
                        user{
                            name
                        }
                        phone_number
                        address
                        position
                    }
                }
            }'''
        self.input = {
            "id":ProfileFactory.create().id,
            "user":UserFactory().id,
            "position":"Developer",
        }

        def test_valid_profile_update(self):
            response = self.query(
                self.mutation,
                input_data=self.input
            )
            content = json.loads(response.content)
            
            self.assertResponseNoErrors(content)
            self.assertTrue(content['data']['UpdateProfile']['ok'], content)
            self.assertIsNone(content['data']['UpdateProfile']['errors'], content)
            self.assertEqual(content['data']['UpdateProfile']['profile']['id'],
                            self.input['id'])
            self.assertEqual(content['data']['UpdateProfile']['profile']['user'],
                            self.input['user'])
            
