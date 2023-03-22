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
        for sale_inv in data.picking_type_id:
            if sale_inv.invoice == True:
                invoice_rec = self.env["sale.advance.payment.inv"].search([])
                for record in invoice_rec:
                    record.create_invoices()

            if sale_inv.invoice == False:
                pass
        return value
