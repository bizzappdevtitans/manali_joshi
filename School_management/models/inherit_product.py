from odoo import fields, models, api


class InheritProduct(models.Model):
    _inherit = "product.product"

    weight_ok = fields.Boolean(string="Weight Done")
    purchase_order_ids = fields.One2many("purchase.order.line", "product_id", limit=5)

    sale_order_ids = fields.One2many("sale.order.line", "product_id", limit=5)
    manufractures_order_ids = fields.One2many("mrp.production", "product_id")

    def get_chatter_attachments(self, sale_order):
        attachments = self.env["ir.attachment"]
        for message in self.message_ids:
            if message.model == "sale.order" and message.res_id == sale_order.id:
                for attachment in message.attachment_ids:
                    attachments |= attachment
        return attachments

    def send_by_email(
        self, sale_order_id, template_id, composition_mode="comment", **kwargs
    ):
        self.ensure_one()
        sale_order = self.env["sale.order"].browse(sale_order_id)
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
        return {
            "name": ("Compose Email"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }


class InheritProducttemplate(models.Model):
    _inherit = "product.template"

    weight_ok = fields.Boolean(string="Weight Done")
