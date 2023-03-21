from datetime import datetime, date
from odoo import api, fields, models


class TimetableStructure(models.Model):
    _name = "timetable.structure"
    _description = "School Management system"

    tename_id = fields.Many2one("school.teachers", "Teacher Name")
    week = fields.Selection(
        [
            ("mon", "Monday"),
            ("tue", "Tuesday"),
            ("wed", "Wednesday"),
            ("thu", "Thursday"),
            ("fri", "Friday"),
            ("sat", "Saturday"),
        ],
        string="WEEK DAY"
    )
    sub = fields.Char(string="Subject Name")
    star = fields.Datetime(string="Start Time")
    end = fields.Datetime(string="End Time")
