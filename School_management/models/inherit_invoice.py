from odoo import fields, models

class SaleInvoice(models.Model):
    _inherit = "account.move"

    invoice_desc = fields.Char(string="Invoice Description")


class InvoiceDown(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    # both methods works for Invoice types downpayment

    # def _prepare_invoice_values(self, order, name, amount, so_line):
    #     invoice_vals = super(InvoiceDown, self)._prepare_invoice_values(order, name, amount, so_line)
    #     invoice_vals["invoice_desc"] = order.invoice_id
    #     return invoice_vals
    
    """ This method is used to pass the value from SO to Invoices"""

    def _create_invoice(self, order, so_line, amount):
        invoice_vals = super(InvoiceDown, self)._create_invoice(order, so_line, amount)
        invoice_vals["invoice_desc"] = order.invoice_id
        return invoice_vals