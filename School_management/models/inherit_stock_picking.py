from odoo import fields, models

class SaleDelivery(models.Model):
    _inherit = "stock.picking"
    delivery = fields.Char(string="Delivery Description")
    Customer_Type = fields.Selection(
        [
            ("new", "New Customer"),
            ("exi", "Existing Customer"),
        ]
    )
    pur_order = fields.Char(string="Purchase Order")
    # weight_ok = fields.Boolean(string="Weight Done")
    weight = fields.Float(string="Weight")