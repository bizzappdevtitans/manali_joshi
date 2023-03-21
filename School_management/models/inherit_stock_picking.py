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
    # sale_line_id=fields.Many2one('sale.order.line')
    # weight_ok = fields.Boolean(string="Weight Done",related="sale_line_id.weight_ok")
    # weight = fields.Float(string="Weight",related="sale_line_id.weight",store=True)
    weight_ok = fields.Boolean(string="Weight Done")
    weight = fields.Float(string="Weight")