from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolAdmission(models.Model):
    _name = "school.admission"
    _description = "School Management system"
    _rec_name = "combination"

    image = fields.Binary()
    first_name = fields.Char(default="")
    last_name = fields.Char(default="")
    combination = fields.Char(
        string="Student Name", compute="_compute_fields_combination"
    )
    birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ]
    )
    Section = fields.Selection(
        [
            ("pri", "Science"),
            ("sec", "Commerce"),
        ]
    )
    science = fields.Selection(
        [
            ("math", "Maths"),
            ("bio", "Biology"),
            ("both", "Both"),
        ]
    )
    commerce = fields.Selection(
        [
            ("all", "All Subjects"),
        ]
    )
    standard = fields.Selection(
        [
            ("11s", "11th Science"),
            ("12s", "12th Science"),
            ("11c", "11th Commerce"),
            ("12c", "12th Commerce"),
        ]
    )
    photo = fields.Binary(string="Upload Image")
    doc = fields.Binary(string="Upload Documents")
    state = fields.Selection(
        [
            ("start", "Reviewing Form"),
            ("mode", "Verifying documents"),
            ("end", "Confirmed"),
        ],
        string="Status",
        required=True,
        readonly=True,
        copy=False,
        default="start",
    )
    reference_no = fields.Char(
        string="Number", required=True, index=True, copy=False, default="New"
    )

    def button_in_progress(self):
        self.write({"state": "end"})

    def btn_done(self):
        return {
            "effect": {
                "fadeout": "slow",
                "message": "****Welcome To Our School****",
                "type": "rainbow_man",
            }
        }
# Combine First name & last name
    @api.depends("first_name", "last_name")
    def _compute_fields_combination(self):
        for test in self:
            test.combination = test.first_name + " " + test.last_name

# Calculate age from Date of birth
    @api.onchange("birth")
    def _compute_age(self):
        for res in self:
            today = date.today()
            if res.birth:
                res.age = today.year - res.birth.year

# Check the age of the student 
    @api.constrains("age")
    def _check_something(self):
        for record in self:
            if record.age < 10:
                raise ValidationError("Age is Less than 10")

# Unlink method for not removing confirmed admissions
    @api.ondelete(at_uninstall=False)
    def _unlink_except_done(self):
        if any(batch.state == "end" for batch in self):
            raise UserError(("You cannot delete Confirmed admission."))
            
# Generate sequence number
    @api.model
    def create(self, vals):
        vals["reference_no"] = self.env["ir.sequence"].next_by_code("school.admission")
        return super(SchoolAdmission, self).create(vals)
