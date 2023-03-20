from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class AssignmentSubmit(models.Model):

    _name = "assignment.submit"
    _description = "School Management system"
    _rec_name ="assigned_id2"

    date = fields.Date(string="Date")
    assigned_id1 = fields.Many2one("school.teachers", "Assinged by")
    assigned_id2 = fields.Many2one("school.students", "Assinged To")
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
        self.states = "mode"
        
    def button_confirm(self):
        self.states = "end"

    def sticky_notification(self):
        action = self.env.ref('School_management.action_assignment_submit')
        notification = {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {'title':('Your Assignment has been submitted'),
                    'message': '%s',
                    'links': [{
                        'label': self.assigned_id2.name,
                        'url': f'#action={action.id}&id={self.assigned_id2.id}&model=assignment.submit',
                    }],
        }
        }
        return notification


    submit = fields.Binary(string="Submit you file here")
    reference = fields.Reference(
        selection=[
            ("school.students", "Student Profile"),
            ("school.assignment", "Student Submission"),
        ],
        string="Details",
    )

    # Override Unlink Function for not removing submitted assignment
    @api.model
    def unlink(self, values):
        if (states == "end" for states in self):
            raise UserError(("You cannot delete Submitted Assignment."))
        override_unlink = super(AssignmentSubmit, self).unlink()
        return override_unlink
