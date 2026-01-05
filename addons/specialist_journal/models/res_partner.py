from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    journal_entry_ids = fields.One2many(
        comodel_name="specialist.journal.entry",
        inverse_name="partner_id",
        string="Specialist Journal",
    )

    journal_entry_count = fields.Integer(
        string="Journal Entries",
        compute="_compute_journal_entry_count",
    )

    def _compute_journal_entry_count(self):
        Entry = self.env["specialist.journal.entry"]
        for partner in self:
            partner.journal_entry_count = Entry.search_count(
                [("partner_id", "=", partner.id)]
                )
