from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import re


class SchoolParents(models.Model):
    _name = "school.parents"
    _description = "School Management system"

    name = fields.Char(string="Father Name")
    names = fields.Char(string="Mother Name")
    parentof_id = fields.Many2one("school.students", "Student Name")
    email = fields.Char(string="Parent Email")
    phone = fields.Char(string="Father's Contact No.")
    phones = fields.Char(string="Mother's Contact No.")
    address = fields.Text(string="Address")
    qualification = fields.Char(string="Father's Qualification")
    qualifications = fields.Char(string="Mother's Qualification")
    Range = fields.Selection(
        [
            ("less", "Income Less Than 1 lac"),
            ("more", "Income More Than 1 lac"),
            ("other", "Others"),
        ]
    )

    # Email Validation

    @api.onchange("email")
    def validate_mail(self):
       if self.email:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
        if match == None:
            raise ValidationError('Not a valid E-mail ID')

    # Phone Validation
    @api.constrains("phone")
    def _check_phone(self):
        for values in self:
            if values.phone and not str(values.phone).isdigit():
                raise ValidationError(("Cannot enter Characters"))
            if len(values.phone) != 10:
                raise ValidationError("Invalid Number")

    @api.constrains("phones")
    def _check_number(self):
        for values in self:
            if values.phones and not str(values.phones).isdigit():
                raise ValidationError(("Cannot enter Characters"))
            if len(values.phones) != 10:
                raise ValidationError("Invalid Number")

    teachname = fields.Many2many("school.teachers", string="Teacher Details")
    Teacher_count = fields.Integer(compute="compute_count")

    def get_teachers(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Details",
            "view_mode": "tree,form",
            "res_model": "school.teachers",
            "domain": [("id", "in", self.teachname.ids)],
            "context": "{'create': False}",
        }

    def compute_count(self):
        for record in self:
            record.Teacher_count = self.env["school.teachers"].search_count(
                [("id", "in", self.teachname.ids)]
            )
