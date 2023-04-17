from odoo import api, fields, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    product_attachments = fields.Many2many(
        "ir.attachment", string="Product Attachments"
    )
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")

    sale_order_line_products = fields.Text(
        string="Products Details", compute="compute_sale_order_lines"
    )

    @api.depends("model", "res_id")
    def compute_sale_order_lines(self):
        for wizard in self:
            if wizard.model == "sale.order":
                sale_order = self.env["sale.order"].browse(wizard.res_id)
                lines = ""
                for line in sale_order.order_line:
                    lines += (
                        line.product_id.display_name
                        + "("
                        + str(line.product_uom_qty)
                        + ")"
                        + "("
                        + str(line.price_unit)
                        + ")\n"
                    )
                wizard.sale_order_line_products = lines

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if (
            res.get("res_id")
            and res.get("model")
            and res.get("composition_mode", "") != "mass_mail"
            and not res.get("can_attach_attachment")
        ):
            res["can_attach_attachment"] = True
        return res

    can_attach_attachment = fields.Boolean()
    object_attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        relation="mail_compose_message_ir_attachments_object_rel",
        column1="wizard_id",
        column2="attachment_id",
        string="Object Attachments",
    )

    def get_mail_values(self, res_ids):
        res = super().get_mail_values(res_ids)
        if self.object_attachment_ids.ids and self.model and len(res_ids) == 1:
            res[res_ids[0]].setdefault("attachment_ids", []).extend(
                self.object_attachment_ids.ids
            )
        if self.product_attachments.ids and self.model and len(res_ids) == 1:
            res[res_ids[0]].setdefault("attachment_ids", []).extend(
                self.product_attachments.ids
            )
        return res
