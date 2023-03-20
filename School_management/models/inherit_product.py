from odoo import fields, models


class InheritProduct(models.Model):
    _inherit = "product.product"

    weight_ok = fields.Boolean(string="Weight Done")


class InheritProducttemplate(models.Model):
    _inherit = "product.template"

    weight_ok = fields.Boolean(string="Weight Done")
