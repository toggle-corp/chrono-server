from datetime import datetime, time

from django.core.exceptions import ValidationError

from task.models import TimeEntry
from utils.factories import TaskFactory, TimeEntryFactory, UserFactory
from utils.tests import ChronoGraphQLTestCase


class TestTimeEntryModel(ChronoGraphQLTestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.data = {
            "description": "for the test",
            "date": "2020-10-10",
            "start_time": "10:10:19",
            "end_time": "12:10:10",
            "task": TaskFactory(),
            "user": self.user
        }

    def test_valid_clean(self):
        time_entry = TimeEntry(**self.data)
        self.assertIsNone(time_entry.clean())

    def test_invalid_clean_end_time_smaller_than_start_time(self):
        self.data['end_time'] = '10:30:25'
        self.data['start_time'] = '11:30:25'
        errors = TimeEntry.clean_dates(self.data)
        self.assertIn('end_time', errors)

    def test_invalid_time_overlap_in_date(self):
        timeentry1 = TimeEntryFactory.create(
            date='2020-10-10',
            start_time='10:10:19',
            end_time='15:10:26',
            user=self.user
        )
        errors = TimeEntry.clean_dates(self.data, timeentry1)
        self.assertIn('date', errors)

    def test_duration(self):
        timeentry = TimeEntryFactory()
        timeentry.date = datetime.now().date()
        timeentry.start_time = time(10, 10, 10)
        timeentry.end_time = time(20, 10, 20)
        timeentry.user = self.user
        timeentry.save()

        difference = datetime.combine(timeentry.date, timeentry.end_time) - \
            datetime.combine(timeentry.date, timeentry.start_time)

        self.assertEqual(timeentry.duration, difference)
