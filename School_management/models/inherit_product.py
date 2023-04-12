from odoo import fields, models


class InheritProduct(models.Model):
    _inherit = "product.product"

    weight_ok = fields.Boolean(string="Weight Done")
    purchase_order_ids = fields.One2many("purchase.order.line", "product_id", limit=5)

    sale_order_ids = fields.One2many("sale.order.line", "product_id", limit=5)
    manufractures_order_ids = fields.One2many("mrp.production", "product_id")


class InheritProducttemplate(models.Model):
    _inherit = "product.template"

    weight_ok = fields.Boolean(string="Weight Done")
