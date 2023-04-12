from odoo import api, fields, models, Command


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

    # def action_quotation_send(self):
    #     ctx = {
    #         "default_template_id": int(
    #             self.env["res.users"].search([]).default_so_template_id
    #         ),
    #     }
    #     return {
    #         "type": "ir.actions.act_window",
    #         "view_mode": "form",
    #         "res_model": "mail.compose.message",
    #         "views": [(False, "form")],
    #         "view_id": False,
    #         "target": "new",
    #         "context": ctx,
    #     }

    # def get_chatter_attachments(self):
    #     attachments = self.env["ir.attachment"].search(
    #         [
    #             ("res_model", "=", self.sale.order),
    #             ("res_id", "=", self.id),
    #             ("res_fields", "=", False),
    #         ]
    #     )
    #     return attachments

    # def action_confirm(self):
    #     template_id = self.env.ref("sale.email_template_edi_sale").id
    #     attachment_id = self.get_chatter_attachments().ids
    #     if template_id:
    #         self.message_post(
    #             body=_("Mail Attachment"),
    #             subtype="mail.mt_comment",
    #             partner_ids=self.partner_id.ids,
    #             template_id=template_id,
    #             attachment_ids=attachment_id,
    #         )
    #         return True

    # def action_send_mail(self):
    #     template_id = self.env.ref("sale.email_template_edi_sale").id
    #     attachment_id = self.get_chatter_attachments().ids
    #     ctx = {
    #         "default_model": "sale.order",
    #         "default_res_id": self.id,
    #         "default_use_template": bool(template_id),
    #         "default_template_id": template_id,
    #         "default_composition_mode": "comment",
    #         "default_attachments_ids": [(6, 0, attachment_id)],
    #         "custom_layout": "mail.mail_notification_light",
    #         "force_email": True,
    #     }
    #     return {
    #         "type": "ir.actions.act_window",
    #         "view_mode": "form",
    #         "res_model": "mail.compose.message",
    #         "target": "new",
    #         "context": ctx,
    #     }

    # def action_quotation_send(self):
    #     ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
    #     self.ensure_one()
    #     attachment_ids = self.env["mail.message"].search([
    #                 ("model", "=", self._name),
    #                 ("res_id", "=", self.id),
    #                 ("attachment_ids", "!=", False),
    #             ]).mapped("attachment_ids").ids
    #     template_id = self._find_mail_template()
    #     lang = self.env.context.get('lang')
    #     template = self.env['mail.template'].browse(template_id)
    #     if template.lang:
    #         lang = template._render_lang(self.ids)[self.id]
    #     ctx = {
    #         'default_model': 'sale.order',
    #         'default_res_id': self.ids[0],
    #         'default_use_template': bool(template_id),
    #         'default_template_id': template_id,
    #         'default_composition_mode': 'comment',
    #         'mark_so_as_sent': True,
    #         'custom_layout': "mail.mail_notification_paynow",
    #         'proforma': self.env.context.get('proforma', False),
    #         'force_email': True,
    #         'attachment_ids': [(6, 0, attachment_ids)],
    #         'model_description': self.with_context(lang=lang).type_name,
    #     }
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'mail.compose.message',
    #         'target': 'new',
    #         'context': ctx,
    #     }

    # def action_quotation_send(self):
    #     attachment_ids = (
    #         self.env["mail.message"]
    #         .search(
    #             [
    #                 ("model", "=", self._name),
    #                 ("res_id", "=", self.id),
    #                 ("attachment_ids", "!=", False),
    #             ]
    #         )
    #         .mapped("attachment_ids")
    #         .ids
    #     )
    #     ctx.update({"attachment_ids": [(6, 0, attachment_ids)]})
    #     return {
    #         "type": "ir.actions.act_window",
    #         "view_mode": "form",
    #         "res_model": "mail.compose.message",
    #         "target": "new",
    #         "context": ctx,
    #     }

    # def send_email_chatter(self):
    #     self.ensure_one()
    #     message = self.message_ids.sorted(key=lambda r: r.id, reverse=True)[0]
    #     attachment_ids = []
    #     for attachment in self.message.attachment_ids:
    #         attachment_ids.append(attachment.id)
    #         for attachment in self.env["ir.attachment"].search(
    #             [("res_model", "=", "sale.order"), ("res_id", "=", self.id)]
    #         ):
    #             attachment_ids.append(attachment.id)
    #             template_id = self.env.ref("sale.email_template_edi_sale").id
    #             compose_form = self.env.ref(
    #                 "mail.email_compose_message_wizard_form", raise_if_not_found=False
    #             )
    #             ctx = dict(
    #                 default_model="sale.order",
    #                 default_res_id=self.id,
    #                 default_use_template=bool(template_id),
    #                 default_template_id=template_id,
    #                 default_composition_mode="comment",
    #                 mark_so_as_sent=True,
    #                 custom_layout="mail.mail_notification_light",
    #                 force_email=True,
    #                 attachment_ids=attachment_ids,
    #             )
    #             return {
    #                 "type": "ir.actions.act_window",
    #                 "view_type": "form",
    #                 "view_mode": "form",
    #                 "res_model": "mail.compose.message",
    #                 "views": [(compose_form.id, "form")],
    #                 "view_id": compose_form.id,
    #                 "target": "new",
    #                 "context": ctx,
    #             }

    # def action_quotation_send(self):
    #     self.ensure_one()
    #     attachment_ids = []
    #     for attachment in self.message_ids:
    #         attachment_ids.append(attachment.id)
    #         for attachment in self.env["ir.attachment"].search(
    #             [("res_model", "=", "sale.order"), ("res_id", "=", self.id)]
    #         ):
    #             attachment_ids.append(attachment.id)
    #             template_id = self.env.ref("sale.email_template_edi_sale").id
    #             ctx = dict(
    #                 default_model="sale.order",
    #                 default_res_id=self.id,
    #                 default_use_template=bool(template_id),
    #                 default_template_id=template_id,
    #                 default_composition_mode="comment",
    #                 mark_so_as_sent=True,
    #                 custom_layout="mail.mail_notification_light",
    #                 force_email=True,
    #                 attachment_ids=attachment_ids,
    #             )
    #             self.message_post_with_template(
    #                 template_id,
    #                 composition_mode="comment",
    #                 email_layout_xmlid="mail.mail_notification_light",
    #                 attachment_ids=attachment_ids)
    #         return True

    # def action_quotation_send(self):
    #     """Opens a wizard to compose an email, with relevant mail template loaded by default"""
    #     self.ensure_one()
    #     attachment = self.env["ir.attachment"].create(
    #         {
    #             "name": self.name + "pdf",
    #             "type": "binary",
    #             # "datas": self.env["report"].get_pdf([self.id], "sale.report_saleorder"),
    #             "res_model": "sale.order",
    #             "res_id": self.id,
    #             "mimetype": "application/pdf",
    #         }
    #     )
    #     self.message_post(
    #         body=("Sale order sent by email."),
    #         attachment_ids=[attachment.id],
    #         message_type="comment",
    #         subtype_xmlid="mail.mt_comment",
    #     )
    #     extra_attachment_data=self.env['ir.attachment'].search([('res_model','=','sale.order'),('res_id','=',self.id)])
    #     attachment_ids = [attachment.id for attachment in extra_attachment_data]
    #     template_id = self.env.ref('sale.email_template_edi_sale').id
    #     compose_form = self.env.ref(
    #         "mail.email_compose_message_wizard_form", raise_if_not_found=False
    #     )
    #     ctx = dict(
    #         default_model="sale.order",
    #         default_res_id=self.ids[0],
    #         # For the sake of consistency we need a default_res_model if
    #         # default_res_id is set. Not renaming default_model as it can
    #         # create many side-effects.
    #         default_use_template=bool(template_id),
    #         default_template_id=template_id,
    #         default_composition_mode="comment",
    #         mark_so_as_sent=True,
    #         custom_layout="mail.mail_notification_paynow",
    #         force_email=True,
    #         attachment_ids=attachment_ids,
    #     )
    #     return {
    #         "type": "ir.actions.act_window",
    #         "view_type": "form",
    #         "view_mode": "form",
    #         "res_model": "mail.compose.message",
    #         "views": [(compose_form.id, "form")],
    #         "view_id": compose_form.id,
    #         "target": "new",
    #         "context": ctx,
    #     }

    """ This method is used to pass the value from SO to Regular Invoice"""

    def _prepare_invoice(self):
        invoice_vals = super(SchoolDescription, self)._prepare_invoice()
        invoice_vals["invoice_desc"] = self.invoice_id
        return invoice_vals


# def _purchase_service_prepare_order_values(self, supplierinfo):
#     vals = super(SchoolDescription, self)._purchase_service_prepare_order_values(supplierinfo)
#     vals["pur_order"] = self.pur_order
#     return vals
