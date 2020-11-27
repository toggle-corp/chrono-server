import json
from datetime import datetime, timedelta, time


from utils.tests import ChronoGraphQLTestCase
from utils.factories import (
    UserFactory,
    TaskGroupFactory,
    TaskFactory,
    TimeEntryFactory,
    ProjectFactory,
)


"""
Test case for Task model mutations and query
"""


class TestCreateTask(ChronoGraphQLTestCase):
    def setUp(self):
        self.user = UserFactory.create().id
        self.mutation = '''mutation CreateTask($input: TaskCreateInputType!){
            createTask(data: $input){
                errors {
                    field
                    messages
                }
                result {
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
        self.assertEqual(content['data']['createTask']['result']['title'],
                         self.input['title'])
        self.assertEqual(content['data']['createTask']['result']['createdBy']['id'], 
                          str(self.input['createdBy']))


class TestUpdateTask(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation UpdateTask($input: TaskUpdateInputType!){
            updateTask(data: $input){
                errors {
                    field
                    messages
                }
                result {
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
        self.assertEqual(content['data']['updateTask']['result']['id'],
                         str(self.input['id']))
        self.assertEqual(content['data']['updateTask']['result']['user']['id'],
                         str(self.input['user']))


class TestDeleteTask(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation DeleteTask($id: ID!){
            deleteTask(id: $id){
                errors {
                    field
                    messages
                }
                result {
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
        self.assertEqual(content['data']['deleteTask']['result']['title'],
                         self.task.title)
        self.assertEqual(int(content['data']['deleteTask']['result']['id']),
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
            createTaskgroup(data: $input){
                errors {
                    field
                    messages
                }
                result {
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
            "project": ProjectFactory.create().id,
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
        self.assertEqual(content['data']['createTaskgroup']['result']['title'],
                         self.input['title'])
        self.assertEqual(content['data']['createTaskgroup']['result']['createdBy']['id'],
                          str(self.input['createdBy']))


class TaskGroupUpdate(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation UpdateTaskGroup($input: TaskGroupUpdateInputType!){
            updateTaskgroup(data: $input){
                errors {
                    field
                    messages
                }
                result {
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
        self.assertEqual(content['data']['updateTaskgroup']['result']['id'],
                         str(self.input['id']))
        self.assertEqual(content['data']['updateTaskgroup']['result']['users'][0]['id'],
                         str(self.input['users']))


class TestDeleteTaskGroup(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation DeleteTaskGroup($id: ID!){
            deleteTaskgroup(id: $id){
                errors {
                    field
                    messages
                }
                result {
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
        self.assertEqual(content['data']['deleteTaskgroup']['result']['title'],
                         self.taskGroup.title)
        self.assertEqual(int(content['data']['deleteTaskgroup']['result']['id']),
                         self.taskGroup.id)


"""
Test Case for the TimeEntry
"""


class TimeEntryCreate(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation CreateTimeEntry($input: TimeEntryCreateInputType!){
            createTimeentry(data: $input){
                errors {
                    field
                    messages
                }
                result {
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
        self.assertEqual(content['data']['createTimeentry']['result']['task']['id'],
                         str(self.input['task']))


class UpdateTimeEntry(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation UpdateTimeEntry($input: TimeEntryUpdateInputType!){
            updateTimeentry(data: $input){
                errors {
                    field
                    messages
                }
                result {
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
        self.assertEqual(content['data']['updateTimeentry']['result']['task']['id'],
                         str(self.input['task']))
        self.assertEqual(content['data']['updateTimeentry']['result']['id'],
                         str(self.input['id']))


class DeleteTimeEntry(ChronoGraphQLTestCase):
    def setUp(self):
        self.mutation = '''mutation DeleteTimeEntry($id: ID!){
            deleteTimeentry(id: $id){
                errors {
                    field
                    messages
                }
                result {
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
        self.assertEqual(content['data']['deleteTimeentry']['result']['description'],
                         self.timeEntry.description)
        self.assertEqual(int(content['data']['deleteTimeentry']['result']['id']),
                         self.timeEntry.id)


"""Summary api"""


class TestSummaryAPI(ChronoGraphQLTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.force_login(self.user)
        self.task1 = TaskFactory.create(
            user=self.user,
        )
        self.task2 = TaskFactory.create(
            user=self.user
        )
        self.timeentry1 = TimeEntryFactory.create(
            date=datetime.now().date() + timedelta(days=2),
            start_time=time(10, 10, 10),
            end_time=time(12, 10, 10),
            user=self.user,
            task=self.task1,
        )
        self.timeentry2 = TimeEntryFactory.create(
            date=datetime.now().date() + timedelta(days=3),
            start_time=time(10, 10, 10),
            end_time=time(20, 10, 10),
            user=self.user,
            task=self.task2,
        )

        # same day for differet task
        self.timeentry3 = TimeEntryFactory.create(
            date=datetime.now().date() + timedelta(days=2),
            start_time=time(15, 10, 10),
            end_time=time(20, 10, 10),
            user=self.user,
            task=self.task2,
        )

        # create timeentry for the next month
        self.timeentry4 = TimeEntryFactory.create(
            date=datetime.now().date() + timedelta(days=20),
            start_time=time(15, 10, 10),
            end_time=time(20, 10, 10),
            user=self.user,
            task=self.task2,
        )

        self.q = """
            query SummaryWeekly{
                summaryWeekly {
                    totalHoursWeekly
                    totalHoursDay {
                        date
                        durationDay
                        taskList {
                            id
                            duration
                        }
                    }
                }
            }
        """

        self.q1 = """
            query SummaryMonthly{
                summaryMonthly {
                    totalHoursMonthly
                    totalHoursDay {
                        date
                        durationDay
                        taskList {
                            id
                            duration
                        }
                    }
                }
            }

        """

    def test_weekly_summary_api_reponse_structure(self):
        response = self.query(
            self.q
        )

        hours1 = datetime.combine(self.timeentry1.date, self.timeentry1.end_time)\
                - datetime.combine(self.timeentry1.date, self.timeentry1.start_time)

        hour2 = datetime.combine(self.timeentry2.date, self.timeentry2.end_time)\
                - datetime.combine(self.timeentry2.date, self.timeentry2.start_time)
        hour3 = datetime.combine(self.timeentry3.date, self.timeentry3.end_time)\
                - datetime.combine(self.timeentry3.date, self.timeentry3.start_time)

        HOURS_TOTAL = hours1 + hour2 + hour3

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['summaryWeekly']['totalHoursWeekly'], str(HOURS_TOTAL))
        self.assertEqual(content['data']['summaryWeekly']['totalHoursDay'][0]['date'],
        str(self.timeentry1.date))

    def test_monthly_summary_api_reponse_structure(self):
        response = self.query(
            self.q1
        )

        hours1 = datetime.combine(self.timeentry1.date, self.timeentry1.end_time)\
                - datetime.combine(self.timeentry1.date, self.timeentry1.start_time)

        hour2 = datetime.combine(self.timeentry2.date, self.timeentry2.end_time)\
                - datetime.combine(self.timeentry2.date, self.timeentry2.start_time)
        hour3 = datetime.combine(self.timeentry3.date, self.timeentry3.end_time)\
                - datetime.combine(self.timeentry3.date, self.timeentry3.start_time)

        HOURS_TOTAL = hours1 + hour2 + hour3
        HOURS_DAY = hours1 + hour3

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['summaryMonthly']['totalHoursMonthly'], str(HOURS_TOTAL))
        self.assertEqual(content['data']['summaryMonthly']['totalHoursDay'][0]['date'],
        str(self.timeentry1.date))
        self.assertEqual(content['data']['summaryMonthly']['totalHoursDay'][0]['durationDay'],
        str(HOURS_DAY))

    def test_monthly_summary_with_timeentry_another_month(self):
        response = self.query(
            self.q1
        )

        hours1 = datetime.combine(self.timeentry1.date, self.timeentry1.end_time)\
                - datetime.combine(self.timeentry1.date, self.timeentry1.start_time)

        hour2 = datetime.combine(self.timeentry2.date, self.timeentry2.end_time)\
                - datetime.combine(self.timeentry2.date, self.timeentry2.start_time)
        hour3 = datetime.combine(self.timeentry3.date, self.timeentry3.end_time)\
                - datetime.combine(self.timeentry3.date, self.timeentry3.start_time)
        hour4 = datetime.combine(self.timeentry4.date, self.timeentry4.end_time)\
                - datetime.combine(self.timeentry4.date, self.timeentry4.start_time)


        HOURS_TOTAL = hours1 + hour2 + hour3 + hour4

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertNotEqual(content['data']['summaryMonthly']['totalHoursMonthly'], str(HOURS_TOTAL))
