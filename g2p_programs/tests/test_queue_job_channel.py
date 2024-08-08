import logging

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestCustomQueueJobChannel(TransactionCase):
    def setUp(self):
        super().setUp()
        self.queue_job_channel_model = self.env['queue.job.channel']

    def test_01_valid_record_creation(self):
        # Record not starting with "root" can be created with parent
        child_channel = None
        parent_channel = self.queue_job_channel_model.create({'name': 'root_parent'})
        child_channel = self.queue_job_channel_model.create({
            'name': 'child_channel',
            'parent_id': parent_channel.id
        })

        self.assertIsNotNone(child_channel)

    def test_02_valid_record_creation(self):
        # Record starting with "root" can be created without parent
        root_channel = None
        root_channel = self.queue_job_channel_model.create({'name': 'root_channel'})

        self.assertIsNotNone(root_channel)

    def test_01_invalid_record_creation(self):
        # Record not starting with 'root' cannot be created without parent
        with self.assertRaises(ValidationError, msg="Parent channel required."):
            self.queue_job_channel_model.create({'name': 'child_channel'})

