from odoo import api, fields, models


class SchoolDescription(models.Model):
    _inherit = "sale.order"

    Customer_Type = fields.Selection(
        [
            ("new", "New Customer"),
            ("exi", "Existing Customer"),
        ]
    )
    delivery = fields.Char(string="Delivery Description")
    invoice_id = fields.Char(string="Invoice Description")
    project_desc = fields.Char(string="Project Description")
    pur_order = fields.Char(string="Purchase Order")
    mrp_order = fields.Char(string="Manufacturing")

    """ This method is used to pass the value from SO to Regular Invoice"""

    def _prepare_invoice(self):
        invoice_vals = super(SchoolDescription, self)._prepare_invoice()
        invoice_vals["invoice_desc"] = self.invoice_id
        return invoice_vals

    # def _purchase_service_prepare_order_values(self, supplierinfo):
    #     vals = super(SchoolDescription, self)._purchase_service_prepare_order_values(supplierinfo)
    #     vals["pur_order"] = self.pur_order
    #     return vals
