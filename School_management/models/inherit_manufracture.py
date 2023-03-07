from odoo import fields, models

class MoInherit(models.Model):
    _inherit = "mrp.production"

    mrp_order = fields.Char(string="Manufacturing")
