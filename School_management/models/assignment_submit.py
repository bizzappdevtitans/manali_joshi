from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class AssignmentSubmit(models.Model):

    _name = "assignment.submit"
    _description = "School Management system"

    date = fields.Date(string="Date")
    assigned1 = fields.Many2one("school.teachers", "Assinged by")
    assigned_id1 = fields.Many2one("school.students", "Assinged To")
    Type = fields.Selection(
        [
            ("soft", "Soft Copy"),
            ("hard", "Hard Copy"),
        ]
    )
    subject = fields.Char(string="Subject")
    deadline = fields.Datetime(string="Deadline")
    desc = fields.Text()
    states = fields.Selection(
        [
            ("start", "Started"),
            ("mode", "In Progress Mode"),
            ("end", "Completed"),
        ],
        string="Status",
        required=True,
        readonly=True,
        copy=False,
        default="start",
    )

    def button_in_progress(self):
        self.write({"states": "end"})

    submit = fields.Binary(string="Submit you file here")
    reference = fields.Reference(
        selection=[
            ("school.students", "Student Profile"),
            ("school.assignment", "Student Submission"),
        ],
        string="Details",
    )

    # Override Unlink Function
    @api.model
    def unlink(self, values):
        if (states == "end" for states in self):
            raise UserError(("You cannot delete Submitted Assignment."))
        override_unlink = super(AssignmentSubmit, self).unlink()
        return override_unlink
