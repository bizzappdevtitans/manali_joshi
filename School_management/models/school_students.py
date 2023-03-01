from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re


class SchoolStudents(models.Model):
    _name = "school.students"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "School Management system"

    standard = standard = fields.Selection(
        [
            ("11s", "11th Science"),
            ("12s", "12th Science"),
            ("11c", "11th Commerce"),
            ("12c", "12th Commerce"),
        ]
    )
    name = fields.Char(string="Students Name")
    birthdate = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ]
    )
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
    Section = fields.Selection(
        [
            ("pri", "Science"),
            ("sec", "Commerce"),
        ]
    )
    photo = fields.Binary(string="Upload Image")

    result = fields.One2many("students.results", "name_id", "Result")
    Total_count = fields.Integer(compute="compute_count")

    stui_id = fields.Char(
        string="Student Id",
        required=True,
        index=True,
        copy=False,
        default="New"
    )

    api.depends("birthdate")

    def _compute_age(self):
        for res in self:
            today = date.today()
            if res.birthdate:
                res.age = today.year - res.birthdate.year

    def get_vehicles(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Result",
            "view_mode": "tree,form",
            "res_model": "students.results",
            "domain": [("eligible", "=", self.id)],
            "context": "{'create': False}",
        }

    # ORM search count

    def compute_count(self):
        for record in self:
            record.Total_count = self.env["students.results"].search_count(
                [("eligible", "=", self.id)]
            )

    # ORM BROWSE METHOD

    def action_browse(self):
        for rec in self:
            student = self.env["school.students"].browse(32)
            print(student.name)

    # Name search method

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if name:
            args += [
                "|",
                "|",
                ("name", operator, name),
                ("email", operator, name),
                ("stui_id", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return super(SchoolStudents, self)._name_search(
            name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )

# sequence generate for student id
    @api.model
    def create(self, vals):
        vals['stui_id'] = self.env['ir.sequence'].next_by_code('school.students')
        return super(SchoolStudents, self).create(vals)


