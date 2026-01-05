from odoo import api, fields, models, _
from odoo.exceptions import AccessError
from datetime import timedelta


class SpecialistJournalEntry(models.Model):
    _name = "specialist.journal.entry"
    _description = "Specialist Journal Entry"
    _order = "date desc, id desc"

    name = fields.Char(string="Title")
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Client",
        required=True,
        ondelete="cascade",
        index=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Specialist",
        required=True,
        default=lambda self: self.env.user,
        index=True,
    )
    date = fields.Datetime(
        string="Entry Date",
        required=True,
        default=fields.Datetime.now,
        index=True,
    )
    entry_type = fields.Selection(
        selection=[
            ("consultation", "Consultation"),
            ("follow_up", "Follow-up"),
            ("call", "Call"),
            ("issue", "Issue"),
            ("closure", "Case closure"),
        ],
        string="Type",
        default="consultation",
        required=True,
        index=True,
    )
    template_ids = fields.Many2many(
        comodel_name="specialist.journal.template",
        string="Templates",
    )

    content = fields.Text(string="Notes")

    @api.onchange("entry_type")
    def _onchange_entry_type_set_default_title(self):
        for rec in self:
            if not rec.name and rec.entry_type:
                rec.name = dict(
                    self._fields["entry_type"].selection
                    ).get(rec.entry_type)

    @api.onchange("template_ids")
    def _onchange_template_ids_apply(self):
        for rec in self:
            if not rec.template_ids:
                continue

            for tpl in rec.template_ids:
                if tpl.entry_type:
                    rec.entry_type = tpl.entry_type
                    break

    def _get_edit_window_hours(self) -> int:
        val = self.env["ir.config_parameter"].sudo().get_param(
            "specialist_journal.edit_window_hours", default="0" 
        )
        try:
            hours = int(val)
        except Exception:
            hours = 0
        return max(hours, 0)

    def _check_user_can_write(self):
        hours = self._get_edit_window_hours()
        now = fields.Datetime.now()

        for rec in self:
            if rec.user_id != self.env.user:
                raise AccessError(
                    _("You can edit only your own journal entries.")
                    )

            if hours > 0 and rec.create_date:
                deadline = rec.create_date + timedelta(hours=hours)
                if now > deadline:
                    raise AccessError(
                        _(
                            "Editing window expired. You can edit entries only within %s hour(s) after creation."
                        )
                        % hours
                    )

    def write(self, vals):
        self._check_user_can_write()
        return super().write(vals)

    def unlink(self):
        self._check_user_can_write()
        return super().unlink()

    def action_apply_templates(self):
        for rec in self:
            parts = [t.body for t in rec.template_ids if t.body]
            if not parts:
                continue

            combined = "\n\n---\n\n".join(parts)

            if rec.content and rec.content.strip():
                rec.content = rec.content.rstrip() + "\n\n---\n\n" + combined
            else:
                rec.content = combined

            if not rec.name:
                rec.name = ", ".join(
                    [ty.name for ty in rec.template_ids if ty.name][:3]
                    )
            if not rec.entry_type:
                for ty in rec.template_ids:
                    if ty.entry_type:
                        rec.entry_type = ty.entry_type
                        break
