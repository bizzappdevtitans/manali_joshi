from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import UserError


class SchoolFees(models.Model):
    _name = "school.fees"
    _description = "School Management system"

    stui_id = fields.Many2one("school.students", "Student Details")
    description = fields.Text(string="Description")
    number = fields.Char(string="Number")
    paydate = fields.Date(string="Date")

    _sql_constraints = [
        ("number_unique", "unique (number)", "Slip No already generated...!")
    ]
