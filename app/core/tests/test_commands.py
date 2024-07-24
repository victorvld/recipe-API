from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# check is provided by the Base Command class that allows to
# check the state of the DB And we want to mock this method to
# simulate the response of the DB
# Mock DB behavior
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):

    # The patched_check is the mock object that we are passing to the test
    # method
    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # beacuase we don't wait in the test, we need to mock the sleep function
    @patch('time.sleep')
    # the arguments order is inside out. The patched_sleep is the first
    # argument and the patched_check is the second.
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # This way we rise an exception instead of returning a value
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
