import logging
from datetime import datetime

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install")
class TestG2PRegistrant(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner_model = cls.env['res.partner']
        cls.program_model = cls.env['g2p.program']
        cls.cycle_model = cls.env["g2p.cycle"]
        cls.program_membership_model = cls.env['g2p.program_membership']
        cls.cycle_membership_model = cls.env['g2p.cycle.membership']
        cls.entitlement_model = cls.env['g2p.entitlement']

        cls.program_1 = cls.program_model.create({"name": "A Program"})
        cls.program_2 = cls.program_model.create({"name": "B Program"})

        cls.cycle_1 = cls.cycle_model.create(
            {
                "name": "Test Cycle 1",
                "program_id": cls.program_1.id,
                "start_date": datetime.now(),
                "end_date": datetime.now(),
            }
        )
        cls.cycle_2 = cls.cycle_model.create(
            {
                "name": "Test Cycle 2",
                "program_id": cls.program_2.id,
                "start_date": datetime.now(),
                "end_date": datetime.now(),
            }
        )

    def test_compute_program_membership_count(self):
        # Computation of program membership count for registrant
        partner = self.partner_model.create({'name': 'John Doe'})
        self.assertTrue(partner)

        program_1 = self.program_model.create({'name': 'A Program'})
        program_2 = self.program_model.create({'name': 'B Program'})
        self.assertTrue(program_1)
        self.assertTrue(program_2)
        
        program_membership_1 = self.program_membership_model.create({'partner_id': partner.id, 'program_id': program_1.id})
        program_membership_2 = self.program_membership_model.create({'partner_id': partner.id, 'program_id': program_2.id})
        self.assertTrue(program_membership_1)
        self.assertTrue(program_membership_2)
        
        self.assertEqual(partner.program_membership_count, 2)

    def test_compute_entitlements_count(self):
        # Computation of program membership count for registrant
        partner = self.partner_model.create({'name': 'John Doe'})
        self.assertTrue(partner)
        
        entitlement_1 = self.entitlement_model.create({
                "partner_id": partner.id,
                "program_id": self.program_1.id,
                "cycle_id": self.cycle_1.id,
                "initial_amount": 1000.0,
                "is_cash_entitlement": True,
                "state": "draft",
            })
        entitlement_2 = self.entitlement_model.create({
                "partner_id": partner.id,
                "program_id": self.program_2.id,
                "cycle_id": self.cycle_2.id,
                "initial_amount": 1000.0,
                "is_cash_entitlement": True,
                "state": "draft",
            })
        self.assertTrue(entitlement_1)
        self.assertTrue(entitlement_2)
        
        # Check entitlements_count
        self.assertEqual(partner.entitlements_count, 2)

    def test_compute_cycle_count(self):
        # Computation of cycle membership count for registrant
        partner = self.partner_model.create({'name': 'Test Partner'})
        self.assertTrue(partner)
        
        cycle_membership_1 = self.cycle_membership_model.create({"partner_id": partner.id, "cycle_id": self.cycle_1.id})
        cycle_membership_2 = self.cycle_membership_model.create({"partner_id": partner.id, "cycle_id": self.cycle_2.id})
        self.assertTrue(cycle_membership_1, "Cycle membership 1 was not created successfully")
        self.assertTrue(cycle_membership_2, "Cycle membership 2 was not created successfully")
        
        # Check if cycles_count is correct
        self.assertEqual(partner.cycles_count, 2, "Cycles count is incorrect")

    def test_01_check_valid_email(self):
        # Raises ValidationError if invalid email is passed      
        with self.assertRaises(ValidationError, msg="Invalid Email! Please enter a valid email address."):
            self.partner_model.create({'name': 'John Doe', 'email': 'invalid_email'})

    def test_02_check_valid_email(self):
        # No ValidationError is raised if valid email is passed
        partner = self.partner_model.create({'name': 'Test Partner', 'email': 'valid@example.com'})
        self.assertTrue(partner)

        try:
            partner._check_valid_email()
        except ValidationError:
            self.fail("Valid email raised ValidationError")