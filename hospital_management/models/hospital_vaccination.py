from odoo import api, fields, models
from datetime import date, datetime


class medical_vaccination(models.Model):
    _name = "hospital.vaccination"
    _description = "hospital vaccination"

    vaccine_product_id = fields.Many2one(
        "product.product", string="Name", required=True
    )
    next_dose_date = fields.Datetime(string="Next Dose")
    vaccine_expiration_date = fields.Datetime(string="Expiration Date", required=True)
    observations = fields.Char(string="Observations")
    dose = fields.Integer(string="Dose Number", required=True)
    date = fields.Datetime(string="Date", required=True)
    vaccine_lot = fields.Char(string="Lot Number")
    medical_patient_vaccines_id = fields.Many2one(
        "hospital.patient", string="Vaccination"
    )
