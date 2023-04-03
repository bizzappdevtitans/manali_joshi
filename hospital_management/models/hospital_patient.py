from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import ValidationError,UserError
import re


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name_seq = fields.Char(
        string="Patient ID",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
    )
    name = fields.Char(string="Patient Name", required=True, tracking=True)
    address = fields.Char(string="Address", tracking=True)
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], default="male", tracking=True
    )
    phone = fields.Char(string="Phone", required=True, tracking=True)
    birth = fields.Date(string="Date of Birth", required=True, tracking=True)
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email", tracking=True)
    patient_blood_group = fields.Selection(
        [
            ("A+", "A+ve"),
            ("B+", "B+ve"),
            ("O+", "O+ve"),
            ("AB+", "AB+ve"),
            ("A-", "A-ve"),
            ("B-", "B-ve"),
            ("O-", "O-ve"),
            ("AB-", "AB-ve"),
        ],
        string="Blood Group",
    )
    patient_name_upper = fields.Char(
        compute="_compute_upper_name",
        inverse="_inverse_upper_name",
        string="Patient Name Upper",
    )
    medical_vaccination_ids = fields.One2many(
        "hospital.vaccination", "medical_patient_vaccines_id"
    )
    patient_appointment_ids = fields.One2many(
        "hospital.appointment", "patient_id", string="Appointment Count", readonly=True
    )
    total_appointments = fields.Integer(
        string="No. of appointments", compute="_compute_appointments"
    )

    # Send Message in whatsapp
    def btn_whatsapp(self):
        message = "BizzAppDev Welcome You"
        wa_api_url = "https://api.whatsapp.com/send?phone=%s&text=%s" % (
            self.phone,
            message,
        )
        return {"type": "ir.actions.act_url", "target": "new", "url": wa_api_url}

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
                ("name_seq", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return super(HospitalPatient, self)._name_search(
            name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )

    # FOR COMPUTE UPPER AND LOWER FILEDS
    @api.depends("name")
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.name.upper() if rec.name else False

    def _inverse_upper_name(self):
        for rec in self:
            rec.name = (
                rec.patient_name_upper.lower() if rec.patient_name_upper else False
            )

    # Action For Email button
    def action_send_email(self):
        template_id = self.env.ref("hospital_management.patient_card_email_template").id
        template = self.env["mail.template"].browse(template_id)
        template.send_mail(self.id, force_send=True)

    # FOR MAKE NEW SEQUENCE
    @api.model
    def create(self, vals):
        if vals.get("name_seq", _("New")) == _("New"):
            vals["name_seq"] = self.env["ir.sequence"].next_by_code(
                "hospital.patient"
            ) or _("New")

        result = super(HospitalPatient, self).create(vals)
        return result

    # Phone validation
    @api.constrains("phone")
    def _check_phone(self):
        for values in self:
            if values.phone and not str(values.phone).isdigit():
                raise ValidationError(("Cannot enter Characters"))
            if len(values.phone) != 10:
                raise ValidationError("Invalid Number")

    # Calculate age from Date of birth
    @api.onchange("birth")
    def _compute_age(self):
        for res in self:
            today = date.today()
            if res.birth:
                res.age = today.year - res.birth.year

    # Check if the patient is already exists based on the patient name and phone number
    @api.constrains("name", "phone")
    def _check_patient_exists(self):
        for record in self:
            patient = self.env["hospital.patient"].search(
                [
                    ("name", "=", record.name),
                    ("phone", "=", record.phone),
                    ("id", "!=", record.id),
                ]
            )
            if patient:
                raise ValidationError(f"Patient {record.name} already exists")

    # Email Validation
    @api.constrains("email")
    def _check_email(self):
        for record in self:
            valid_email = re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                record.email,
            )
            if valid_email is None:
                raise ValidationError("Please provide a valid Email")

    # Check Patients Age
    @api.constrains("age")
    def _check_patient_age(self):
        for record in self:
            if record.age <= 0:
                raise ValidationError("Age must be greater than 0")

    # Compute appointments of individual patient
    def _compute_appointments(self):
        for record in self:
            record.total_appointments = self.env["hospital.appointment"].search_count(
                [("patient_id", "=", record.id)]
            )
            
    # User Error
    @api.constrains("patient_blood_group")
    def button_send(self):
        self.ensure_one()
        if not self.patient_blood_group:
            raise UserError("Please Select the Blood Group.")
            return True

    # Action for smart button
    def action_open_appointments(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Appointments",
            "res_model": "hospital.appointment",
            "domain": [("patient_id", "=", self.id)],
            "context": {"default_patient_id": self.id},
            "view_mode": "tree,form",
            "target": "current",
        }
