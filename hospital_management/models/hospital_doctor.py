from odoo import models, fields, api
from datetime import datetime, date
from odoo.exceptions import ValidationError
import re


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Doctor Name", required=True, tracking=True)
    college = fields.Char(string="College", tracking=True)
    address = fields.Char(string="Address", tracking=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], default="male")
    phone = fields.Char(string="Phone", required=True, tracking=True)
    email = fields.Char(string="Email", required=True, tracking=True)
    birth = fields.Date(string="Date of Birth", required=True, tracking=True)
    department_id = fields.Many2one(
        "hr.department", string="Department", required=True, tracking=True
    )
    view_appointment_ids = fields.One2many(
        "hospital.appointment",
        "appointed_doctor_id",
        string="Appointment Count",
        readonly=True,
    )
    age = fields.Integer(string="Age")
    status = fields.Selection(
        [("fulltime", "Full time"), ("parttime", "Part time")],
        required=True,
        default="fulltime",
        tracking=True,
    )
    note = fields.Text(string="Description")
    joined_from = fields.Date(string="Joined Date", tracking=True)
    image = fields.Binary(string="Image", attachment=True)
    total_appointments = fields.Integer(
        string="Total appointments", compute="_compute_appointments"
    )

    # Action for smart button to view patients details
    def get_patients(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Patient",
            "view_mode": "tree,form",
            "res_model": "hospital.patient",
            "domain": [("patient_name_upper", "=", self.id)],
            "context": "{'create': False}",
        }

    # Server Actions
    def action_status_halftime(self):
        self.status = "parttime"

    def action_status_fulltime(self):
        self.status = "fulltime"

    # Email Validation
    @api.constrains("email")
    def _check_email(self):
        for record in self:
            valid_email = re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                record.email,
            )

            if valid_email is None:
                raise ValidationError("Please provide a valid E-mail")

    # Calculate age from Date of birth
    @api.onchange("birth")
    def _compute_age(self):
        for res in self:
            today = date.today()
            if res.birth:
                res.age = today.year - res.birth.year

    # Age Validation
    @api.constrains("age")
    def _check_doctor_age(self):
        for record in self:
            if record.age <= 0:
                raise ValidationError("Age must be greater than 0")

    # Phone validation
    @api.constrains("phone")
    def _check_phone(self):
        for values in self:
            if values.phone and not str(values.phone).isdigit():
                raise ValidationError(("Cannot enter Characters"))
            if len(values.phone) != 10:
                raise ValidationError("Invalid Number")

    # Compute appointments of individual doctor
    def _compute_appointments(self):
        for record in self:
            record.total_appointments = self.env["hospital.appointment"].search_count(
                [("appointed_doctor_id", "=", record.id)]
            )
