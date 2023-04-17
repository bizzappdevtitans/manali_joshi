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

    def send_by_email(self, template_id, composition_mode="comment", **kwargs):
        self.ensure_one()
        products = self.order_line.mapped("product_id")
        attachments = self.env["ir.attachment"]
        for product in products:
            product_attachments = product.get_chatter_attachments(self)
            attachments |= product_attachments
            product.send_by_email(
                self.id, template_id, composition_mode=composition_mode, **kwargs
            )
        compose_form = self.env.ref("mail.email_compose_message_wizard_form", False)
        ctx = dict(
            default_model="product.product",
            default_res_id=self.id,
            default_use_template=bool(template_id),
            default_template_id=template_id,
            default_composition_mode=composition_mode,
            product_attachments=self.get_chatter_attachments(
                sale_order
            ).ids,  # add the attachments here
            sale_order_id=sale_order.id,  # add the sale order id here
            custom_layout="product.mail_template_data_notification_email_product",
            mark_rfq_as_sent=True,
            model_description=self.with_context(lang=self.partner_id.lang)._description,
        )


# def _purchase_service_prepare_order_values(self, supplierinfo):
#     vals = super(SchoolDescription, self)._purchase_service_prepare_order_values(supplierinfo)
#     vals["pur_order"] = self.pur_order
#     return vals
