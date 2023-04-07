from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolAttendance(models.Model):
    _name = "school.attendance"
    _description = "School Management system"

    attend = fields.Char(string="Attend ID")
    date = fields.Date(string="Date")
    names_id = fields.Many2one("school.students", "Name")
    Class = fields.Selection(
        [
            ("stand", "Science"),
            ("stand2", "Commerce"),
        ]
    )
    colour = fields.Integer(string="COLOUR")
    Select = fields.Selection(
        [
            ("pre", "Present"),
            ("abe", "Absent"),
        ]
    )
    referencepro = fields.Reference(
        selection=[
            ("school.students", "Student Profile"),
            ("school.teachers", "Teacher Profile"),
        ],
        string="Details",
    )

    # Date can not be set in past

    @api.constrains("date")
    def _check_date(self):
        for record in self:
            if record.date < fields.Date.today():
                raise ValidationError("The date cannot be set in the past")

    # ORM GETNAME
    @api.model
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s" % (rec.date)))
        return res
