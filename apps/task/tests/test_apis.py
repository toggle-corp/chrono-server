import json

from utils.tests import ChronoGraphQLTestCase
from utils.factories import (
    UserFactory,
    TaskGroupFactory,
    TaskFactory,
    TimeEntryFactory,
)


"""
Test case for Task model mutations and query
"""


class TestCreateTask(ChronoGraphQLTestCase):
    def setUp(self):
        self.user = UserFactory.create().id
        self.mutation = '''mutation CreateTask($input: TaskCreateInputType!){
            createTask(task: $input){
                errors {
                    field
                    messages
                }
                task {
                    id
                    title
                    description
                    user{
                        id
                        email
                    }
                    createdBy{
                        id
                    }
                    modifiedBy{
                        id
                    }
                }
                ok
            }
        }'''

        self.input = {
            "title": "Change the navbar",
            "description": "the existing navbar looks sloopy, change it",
            "createdBy": self.user,
            "modifiedBy": self.user,
            "taskGroup": TaskGroupFactory.create().id,
            "user": self.user,
        }

    def test_valid_task_creation(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createTask']['ok'], content)
        self.assertIsNone(content['data']['createTask']['errors'], content)
        self.assertEqual(content['data']['createTask']['task']['title'],
                         self.input['title'])
        self.assertEqual(content['data']['createTask']['task']['createdBy']['id'], 
                          str(self.input['createdBy']))


class TestUpdateTask(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation UpdateTask($input: TaskUpdateInputType!){
            updateTask(task: $input){
                errors {
                    field
                    messages
                }
                task {
                    id
                    title
                    description
                    user{
                        id
                        email
                    }
                    createdBy{
                        id
                    }
                    modifiedBy{
                        id
                    }
                }
                ok
            }
        }'''

        self.input = {
            "id": TaskFactory.create().id,
            "title": "Change the task view set",
            "taskGroup": TaskGroupFactory.create().id,
            "user": UserFactory.create().id,
        }

    def test_valid_task_update(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['updateTask']['ok'], content)
        self.assertIsNone(content['data']['updateTask']['errors'], content)
        self.assertEqual(content['data']['updateTask']['task']['id'],
                         str(self.input['id']))
        self.assertEqual(content['data']['updateTask']['task']['user']['id'],
                         str(self.input['user']))


class TestDeleteTask(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation DeleteTask($id: ID!){
            deleteTask(id: $id){
                errors {
                    field
                    messages
                }
                task {
                    id
                    title
                    description
                    user{
                        id
                        email
                    }
                    createdBy{
                        id
                    }
                    modifiedBy{
                        id
                    }
                }
                ok
            }
        }'''
        self.task = TaskFactory.create()
        self.variables = {
            "id": self.task.id,
        }

    def test_valid_task_delete(self):
        response = self.query(
            self.mutation,
            variables=self.variables,
        )
        content = json.loads(response.content)
        self.assertTrue(content['data']['deleteTask']['ok'], content)
        self.assertIsNone(content['data']['deleteTask']['errors'], content)
        self.assertEqual(content['data']['deleteTask']['task']['title'],
                         self.task.title)
        self.assertEqual(int(content['data']['deleteTask']['task']['id']),
                         self.task.id)


class TestTaskListQuery(ChronoGraphQLTestCase):
    def setUp(self):
        self.task1_title = 'change the filter'
        self.task1 = TaskFactory.create(title=self.task1_title)
        self.task2 = TaskFactory.create(title='mock-up design')
        self.qy = '''
            query taskList($title:String, $user: ID, $taskGroup: ID){
                taskList(titleContains: $title, user: $user, taskGroup: $taskGroup){
                    id
                }
            }
        '''

    def test_task_list_filter(self):
        variables = {
            "title": self.task1_title,
        }
        response = self.query(
            self.qy,
            variables=variables
        )
        content = json.loads(response.content)
        output = self.task1.id
        self.assertResponseNoErrors(response)
        self.assertEqual(int(content['data']['taskList'][0]['id']), output)

        variables = {
            "taskGroup": self.task1.task_group.id,
        }
        response = self.query(
            self.qy,
            variables=variables,
        )
        content = json.loads(response.content)
        output = self.task1.id
        self.assertResponseNoErrors(response)
        self.assertEqual(int(content['data']['taskList'][0]['id']), output)


"""
Test case for TaskGroup mutations and query
"""


class TestTakGroupCreate(ChronoGraphQLTestCase):
    def setUp(self):
        users = UserFactory.create_batch(2)
        self.user1 = UserFactory.create().id
        self.mutation = '''mutation CreateTaskGroup($input: TaskGroupCreateInputType!){
            createTaskgroup(taskGroup: $input){
                errors {
                    field
                    messages
                }
                taskGroup {
                    id
                    title
                    description
                    users{
                        email
                    }
                    userGroup{
                        id
                    }
                    createdBy{
                        id
                    }
                    modifiedBy{
                        id
                    }
                }
                ok
            }
        }'''

        self.input = {
            "title": "Change the Mis deployment",
            "description": "migrating to Caddy ",
            "status": "INPROGRESS",
            "createdBy": self.user1,
            "modifiedBy": self.user1,
            "users": [i.id for i in users],
            "startDate": "2020-10-01",
            "endDate": "2020-10-20",
        }

    def test_valid_taskgroup_creation(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createTaskgroup']['ok'], content)
        self.assertIsNone(content['data']['createTaskgroup']['errors'], content)
        self.assertEqual(content['data']['createTaskgroup']['taskGroup']['title'],
                         self.input['title'])
        self.assertEqual(content['data']['createTaskgroup']['taskGroup']['createdBy']['id'],
                          str(self.input['createdBy']))


class TaskGroupUpdate(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation UpdateTaskGroup($input: TaskGroupUpdateInputType!){
            updateTaskgroup(taskGroup: $input){
                errors {
                    field
                    messages
                }
                taskGroup {
                    id
                    title
                    description
                    users{
                        id
                        email
                    }
                }
                ok
            }
        }'''

        self.input = {
            "id": TaskGroupFactory.create().id,
            "title": "Change the task view set",
            "users": UserFactory.create().id,
            "status": "DONE",
        }

    def test_valid_taskgroup_update(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['updateTaskgroup']['ok'], content)
        self.assertIsNone(content['data']['updateTaskgroup']['errors'], content)
        self.assertEqual(content['data']['updateTaskgroup']['taskGroup']['id'],
                         str(self.input['id']))
        self.assertEqual(content['data']['updateTaskgroup']['taskGroup']['users'][0]['id'],
                         str(self.input['users']))


class TestDeleteTaskGroup(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation DeleteTaskGroup($id: ID!){
            deleteTaskgroup(id: $id){
                errors {
                    field
                    messages
                }
                taskGroup {
                    id
                    title
                    description
                    users{
                        id
                        email
                    }
                }
                ok
            }
        }'''
        self.taskGroup = TaskGroupFactory.create()
        self.variables = {
            "id": self.taskGroup.id,
        }

    def test_valid_taskgroup_delete(self):
        response = self.query(
            self.mutation,
            variables=self.variables,
        )
        content = json.loads(response.content)
        self.assertTrue(content['data']['deleteTaskgroup']['ok'], content)
        self.assertIsNone(content['data']['deleteTaskgroup']['errors'], content)
        self.assertEqual(content['data']['deleteTaskgroup']['taskGroup']['title'],
                         self.taskGroup.title)
        self.assertEqual(int(content['data']['deleteTaskgroup']['taskGroup']['id']),
                         self.taskGroup.id)


"""
Test Case for the TimeEntry
"""


class TimeEntryCreate(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation CreateTimeEntry($input: TimeEntryCreateInputType!){
            createTimeentry(timeEntry: $input){
                errors {
                    field
                    messages
                }
                timeEntry {
                    id
                    description
                    user{
                        id
                        email
                    }
                    task{
                        id
                    }
                }
                ok
            }
        }'''

        self.input = {
            "description": "change the logo ",
            "user": UserFactory.create().id,
            "task": TaskFactory.create().id,
            "date": "2020-10-10",
            "startTime": "10:10:10"
        }

    def test_valid_taskentry_creation(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['createTimeentry']['ok'], content)
        self.assertIsNone(content['data']['createTimeentry']['errors'], content)
        self.assertEqual(content['data']['createTimeentry']['timeEntry']['task']['id'],
                         str(self.input['task']))


class UpdateTimeEntry(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation UpdateTimeEntry($input: TimeEntryUpdateInputType!){
            updateTimeentry(timeEntry: $input){
                errors {
                    field
                    messages
                }
                timeEntry {
                    id
                    description
                    user{
                        id
                        email
                    }
                    task{
                        id
                    }
                }
                ok
            }
        }'''

        self.input = {
            "id": TimeEntryFactory.create().id,
            "user": UserFactory.create().id,
            "task": TaskFactory.create().id,
            "date": "2020-11-10",
            "startTime": "12:10:10"
        }

    def test_valid_taskentry_update(self):
        response = self.query(
            self.mutation,
            input_data=self.input,
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['updateTimeentry']['ok'], content)
        self.assertIsNone(content['data']['updateTimeentry']['errors'], content)
        self.assertEqual(content['data']['updateTimeentry']['timeEntry']['task']['id'],
                         str(self.input['task']))
        self.assertEqual(content['data']['updateTimeentry']['timeEntry']['id'],
                         str(self.input['id']))


class DeleteTimeEntry(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation DeleteTimeEntry($id: ID!){
            deleteTimeentry(id: $id){
                errors {
                    field
                    messages
                }
                timeEntry {
                    id
                    description
                }
                ok
            }
        }'''

        self.timeEntry = TimeEntryFactory.create()
        self.variables = {
            "id": self.timeEntry.id,
        }

    def test_valid_timeentry_delete(self):
        response = self.query(
            self.mutation,
            variables=self.variables,
        )
        content = json.loads(response.content)
        self.assertTrue(content['data']['deleteTimeentry']['ok'], content)
        self.assertIsNone(content['data']['deleteTimeentry']['errors'], content)
        self.assertEqual(content['data']['deleteTimeentry']['timeEntry']['description'],
                         self.timeEntry.description)
        self.assertEqual(int(content['data']['deleteTimeentry']['timeEntry']['id']),
                         self.timeEntry.id)
