from datetime import datetime
from odoo import fields, models, api


class SchoolAssignment(models.Model):

    _name = "school.assignment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "School Management system"
    _rec_name = "assigned1_id"

    date = fields.Date(string="Date")
    assigned1_id = fields.Many2one("school.teachers", "Assinged by")
    assigned2_id = fields.Many2one("school.students", "Assinged To")
    Type = fields.Selection(
        [
            ("soft", "Soft Copy"),
            ("hard", "Hard Copy"),
        ]
    )
    subject = fields.Char(string="Subject")
    deadline = fields.Datetime(string="Deadline")
    desc = fields.Text(string="Description")

    @api.model
    def deadline_notice_ass(self):
        todays_date = datetime.today().date()
        print("Today's Date", todays_date)
        today_month = todays_date.month
        today_day = todays_date.day
        deadline_ass = self.env["school.assignment"].search([])
        for students_val in deadline_ass:
            if (
                students_val.deadline.month == today_month
                and students_val.deadline.day == today_day
            ):
                print("Deadline is today of the assigned assignment of", students_val.subject)
