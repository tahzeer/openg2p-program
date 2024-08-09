import logging
from datetime import datetime

from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install")
class TestCycleMembership(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.cycle_membership_model = cls.env['g2p.cycle.membership']
        cls.partner_model = cls.env['res.partner']
        cls.program_model = cls.env['g2p.program']
        cls.cycle_model = cls.env['g2p.cycle']

        cls.partner_1 = cls.partner_model.create({'name': 'John Doe'})
        cls.partner_2 = cls.partner_model.create({'name': 'Jane Doe'})
        cls.partner_3 = cls.partner_model.create({'name': 'Group A', 'is_group': True})
        
        cls.program_1 = cls.program_model.create({"name": "A Program"})
        cls.program_2 = cls.program_model.create({"name": "B Program"})

        cls.cycle_1 = cls.cycle_model.create(
            {
                "name": "A Cycle",
                "program_id": cls.program_1.id,
                "start_date": datetime.now(),
                "end_date": datetime.now(),
            }
        )
        cls.cycle_2 = cls.cycle_model.create(
            {
                "name": "B Cycle",
                "program_id": cls.program_2.id,
                "start_date": datetime.now(),
                "end_date": datetime.now(),
            }
        )
    
    def test_01_create_cycle_membership(self):
        # Records with unique (partner_id, cycle_id)
        cycle_member_1 = self.cycle_membership_model.create(
            {
                'partner_id': self.partner_1.id,
                'cycle_id': self.cycle_1.id
            }
        )
        cycle_member_2 = self.cycle_membership_model.create(
            {
                'partner_id': self.partner_1.id,
                'cycle_id': self.cycle_2.id
            }
        )
        cycle_member_3 = self.cycle_membership_model.create(
            {
                'partner_id': self.partner_2.id,
                'cycle_id': self.cycle_2.id
            }
        )

        self.assertTrue(cycle_member_1)
        self.assertTrue(cycle_member_2)
        self.assertTrue(cycle_member_3)
    
    def test_02_create_cycle_membership(self):
        # Record with non-unique (partner_id, cycle_id)
        cycle_member_1 = self.cycle_membership_model.create(
            {
                'partner_id': self.partner_1.id,
                'cycle_id': self.cycle_1.id
            }
        )
        cycle_member_2 = None
        with self.assertRaises(errors.lookup(UNIQUE_VIOLATION)):
            cycle_member_2 = self.cycle_membership_model.create(
                {
                    'partner_id': self.partner_1.id,
                    'cycle_id': self.cycle_1.id
                }
            )
        self.assertTrue(cycle_member_1)
        self.assertIsNone(cycle_member_2)

    def test_compute_display_name(self):
        cycle_membership = self.cycle_membership_model.create(
            {
                'partner_id': self.partner_1.id,
                'cycle_id': self.cycle_1.id
            }
        )
        disp_name = f"[{self.cycle_1.name}] {self.partner_1.name}"

        self.assertEqual(cycle_membership.display_name, disp_name)
    
    def test_open_cycle_membership_form(self):
        cycle_membership = self.cycle_membership_model.create(
            {
                'partner_id': self.partner_1.id,
                'cycle_id': self.cycle_1.id
            }
        )
        form = cycle_membership.open_cycle_membership_form()
        form_expected = {
            "name": "Cycle Membership",
            "view_mode": "form",
            "res_model": "g2p.cycle.membership",
            "res_id": cycle_membership.id,
            "view_id": cycle_membership.env.ref("g2p_programs.view_cycle_membership_form").id,
            "type": "ir.actions.act_window",
            "target": "new",
        }

        self.assertEqual(form, form_expected)

    def test_01_open_registrant_form(self):
        # Open registrant form for individual registrant
        cycle_membership = self.cycle_membership_model.create(
            {
                'partner_id': self.partner_1.id,
                'cycle_id': self.cycle_1.id
            }
        )
        form_data = cycle_membership.open_registrant_form()
        form_data_expected = {
            "name": "Individual Member",
            "view_mode": "form",
            "res_model": "res.partner",
            "res_id": cycle_membership.partner_id.id,
            "view_id": cycle_membership.env.ref("g2p_registry_individual.view_individuals_form").id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {"default_is_group": False},
            "flags": {"mode": "readonly"},
        }
        self.assertEqual(form_data, form_data_expected)

    def test_02_open_registrant_form(self):
        # Open registrant form for group registrant
        cycle_membership = self.cycle_membership_model.create(
            {
                'partner_id': self.partner_3.id,
                'cycle_id': self.cycle_1.id
            }
        )
        form_data = cycle_membership.open_registrant_form()
        form_data_expected = {
            "name": "Group Member",
            "view_mode": "form",
            "res_model": "res.partner",
            "res_id": cycle_membership.partner_id.id,
            "view_id": cycle_membership.env.ref("g2p_registry_group.view_groups_form").id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {"default_is_group": True},
            "flags": {"mode": "readonly"},
        }
        self.assertEqual(form_data, form_data_expected)

    def test_unlink(self):
        cycle_membership_1 = self.cycle_membership_model.create({
            'partner_id': self.partner_1.id,
            'cycle_id': self.cycle_1.id,
        })

        # Test deletion when the cycle is in draft
        cycle_membership_1.unlink()
        self.assertFalse(self.cycle_membership_model.search([('id', '=', cycle_membership_1.id)]))

        # Test deletion when cycle is not in draft
        self.cycle_2.write({'state': 'approved'})
        cycle_membership_2 = self.cycle_membership_model.create({
            'partner_id': self.partner_2.id,
            'cycle_id': self.cycle_2.id,
        })
        with self.assertRaises(ValidationError):
            cycle_membership_2.unlink()