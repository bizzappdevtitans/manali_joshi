from odoo import api, fields, models


class StockImmediateTransfer(models.TransientModel):
    _inherit = "stock.immediate.transfer"

    def process(self):
        value = super(StockImmediateTransfer, self).process()
        data = self.env["stock.picking"].search([])
        for records in data.move_lines:
            sale_order_line_value = records.sale_line_id
            if sale_order_line_value:
                sale_order_line_value["weight"] = records.weight
        return value
