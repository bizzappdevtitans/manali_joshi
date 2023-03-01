from datetime import datetime
from odoo import fields, models


class ExamTimetable(models.Model):
    _name = "exam.timetable"
    _description = "Exam Dates"

    stand = fields.Char("Standard", required=True)
    name = fields.Char("Subject Name", required=True)
    date = fields.Date("Exam Date", required=True)
    date_day = fields.Char("Day")
    year = fields.Date("Year")
    variable = fields.Boolean("Date may change")
    Type = fields.Selection(
        [
            ("theory", "Theory Exam"),
            ("practical", "Practical Exam"),
        ]
    )
