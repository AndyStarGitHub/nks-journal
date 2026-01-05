# -*- coding: utf-8 -*-
from odoo import fields, models


class SpecialistJournalTemplate(models.Model):
    _name = "specialist.journal.template"
    _description = "Specialist Journal Template"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    entry_type = fields.Selection(
        selection=[
            ("consultation", "Consultation"),
            ("follow_up", "Follow-up"),
            ("call", "Call"),
            ("issue", "Issue"),
            ("closure", "Case closure"),
        ],
        string="Default Type",
    )
    body = fields.Text(string="Template Body", required=True)
