from datetime import datetime
from odoo import fields, models


class SchoolAssignment(models.Model):

    _name = "school.assignment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "School Management system"

    date = fields.Date(string="Date")
    assigned = fields.Many2one("school.teachers", "Assinged by")
    assigned_id = fields.Many2one("school.students", "Assinged To")
    Type = fields.Selection(
        [
            ("soft", "Soft Copy"),
            ("hard", "Hard Copy"),
        ]
    )
    subject = fields.Char(string="Subject")
    deadline = fields.Datetime(string="Deadline")
    desc = fields.Text(string="Description")
