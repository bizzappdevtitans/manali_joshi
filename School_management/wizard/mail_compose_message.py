from odoo import api, fields, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"


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
        return res

    # extra_attachment_ids = fields.Many2many("ir.attachment", string="Attachments")

    # def action_send_mail(self):
    #     template = self.env.ref("mail.template_data_notification_email")
    #     for attachment in self.extra_attachment_ids:
    #         attachment_id = self.env["ir.attachment"].create(
    #             {
    #                 "name": attachment.name,
    #                 "datas": attachment.datas,
    #                 "datas_fname": attachment.datas_fname,
    #                 "type": attachment.type,
    #                 "res_model": self._name,
    #                 "res_id": self.id,
    #             }
    #         )
    #         template.attachment_ids |= attachment_id
    #         return super(MailComposeMessage, self).action_send_mail()

    # attachment_ids = fields.Many2many("ir.attachment", string="Attachments")

    # def show_attachment_list(self):
    #     message_ids = self.env["mail.message"].search(
    #         [
    #             ("model", "=", self._context.get("default_model")),
    #             ("res_id", "=", self._context.get("default_res_id")),
    #         ]
    #     )
    #     attachment_ids = message_ids.mapped("attachment_ids").ids
    #     self.attachment_ids = [(6, 0, attachment_ids)]
