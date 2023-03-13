from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolTeachers(models.Model):
    _name = "school.teachers"
    _description = "School Management system"
    _rec_name = "tecname"

    tecname = fields.Char(string="Teacher Name")
    photo = fields.Binary(string="Upload Image")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ]
    )
    email = fields.Char(string="Teacher Email")
    phone = fields.Char(string="Teacher Phone")
    address = fields.Text(string="Teacher Address")
    qualification = fields.Char(string="Teacher Qualification")
    assign = fields.Char(string="Assigned Class")
    # Phone Validation
    @api.constrains("phone")
    def _check_phone(self):
        for record in self:
            if len(record.phone) != 10:
                raise ValidationError("Invalid Number")

    # ORM GET NAME
    @api.model
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s" % (rec.tecname)))
        return res

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if name:
            args += [
                "|",
                "|",
                ("tecname", operator, name),
                ("email", operator, name),
                ("phone", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
