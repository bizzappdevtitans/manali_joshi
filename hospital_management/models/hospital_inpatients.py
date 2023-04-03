from odoo import models, fields, api
from datetime import date, datetime


class HospitalInpatients(models.Model):
    _name = "hospital.inpatients"
    _description = "hospital Inpatients"
    _rec_name = "patient_id"

    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    hospitalization_date = fields.Datetime(string="Hospitalization date", required=True)
    discharge_date = fields.Datetime(string="Expected Discharge date", required=True)
    attending_physician_id = fields.Many2one(
        "hospital.doctor", string="Attending Physician"
    )
    operating_physician_id = fields.Many2one(
        "hospital.doctor", string="Operating Physician"
    )
    admission_type = fields.Selection(
        [
            ("routine", "Routine"),
            ("maternity", "Maternity"),
            ("elective", "Elective"),
            ("urgent", "Urgent"),
            ("emergency", "Emergency  "),
        ],
        required=True,
        string="Admission Type",
    )
    reason = fields.Char(string="Reason for Admission")
    info = fields.Text(string="Extra Info")
    diet_vegetarian = fields.Selection(
        [
            ("none", "None"),
            ("vegetarian", "Vegetarian"),
            ("lacto", "Lacto Vegetarian"),
            ("lactoovo", "Lacto-Ovo-Vegetarian"),
            ("pescetarian", "Pescetarian"),
            ("vegan", "Vegan"),
        ],
        string="Vegetarian",
    )
    nutrition_notes = fields.Text(string="Nutrition notes / Directions")
    state = fields.Selection(
        [
            ("free", "Draft"),
            ("confirmed", "Confirmed"),
            ("hospitalized", "Hospitalized"),
            ("cancel", "Cancel"),
            ("done", "Done"),
        ],
        string="State",
        default="free",
    )
    nursing_plan = fields.Text(string="Nursing Plan")
    discharge_plan = fields.Text(string="Discharge Plan")
    icu = fields.Boolean(string="ICU")
    bed_transfers_ids = fields.One2many(
        "bed.transfer", "inpatient_id", string="Transfer Bed", readonly=True
    )

    # Action for the State
    def registration_confirm(self):
        self.write({"state": "confirmed"})

    def registration_admission(self):
        self.write({"state": "hospitalized"})

    def registration_cancel(self):
        self.write({"state": "cancel"})

    def patient_discharge(self):
        self.write({"state": "done"})


class bed_transfer(models.Model):
    _name = "bed.transfer"
    _description = "Bed Transfer"
    _rec_name = "inpatient_id"

    date = fields.Datetime(string="Date")
    bed_from = fields.Char(string="From")
    bed_to = fields.Char(string="To")
    reason = fields.Text(string="Reason")
    inpatient_id = fields.Many2one("hospital.inpatients", string="Inpatient Id")
