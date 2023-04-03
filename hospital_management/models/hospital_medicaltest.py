from odoo import models, fields, api


class HospitalMedicalTest(models.Model):
    _name = "hospital.medicaltest"
    _description = "Medical Test"
    _rec_name = "product_id"

    product_id = fields.Many2one("product.template", required=True)
    price_unit = fields.Float(string="Price", related="product_id.list_price")
    report_delivery_time = fields.Integer(string="Report Delivery Time")
    medical_test_ids = fields.Many2many(string="Medical tests")
