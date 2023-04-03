from datetime import datetime, date
from odoo.exceptions import ValidationError, UserError
from odoo import models, fields, api, _


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Appointments"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Appointment Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
    )
    patient_id = fields.Many2one(
        "hospital.patient", string="Patient Name", required=True
    )
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], related="patient_id.gender"
    )
    phone = fields.Char(string="Phone", related="patient_id.phone")
    email = fields.Char(string="Email", related="patient_id.email")
    age = fields.Integer(string="Age", related="patient_id.age")
    description = fields.Text()
    note = fields.Text(string="Note")
    inpatient_registration_id = fields.Many2one(
        "hospital.inpatients", string="Inpatient Registration"
    )
    priority = fields.Selection(
        [
            ("0", "normal"),
            ("1", "Low"),
            ("2", "High"),
            ("3", "Very High"),
        ],
        string="priority",
    )
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
            ("done", "Done"),
            ("cancel", "Canceled"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    urgency_level = fields.Selection(
        [
            ("a", "Normal"),
            ("b", "Urgent"),
            ("c", "Medical Emergency"),
        ],
        "Urgency Level",
        sort=False,
        default="b",
    )
    patient_status = fields.Selection(
        [
            ("ambulatory", "Ambulatory"),
            ("outpatient", "Outpatient"),
            ("inpatient", "Inpatient"),
        ],
        "Patient status",
        sort=False,
        default="outpatient",
    )
    appointment_date = fields.Datetime(
        string="Appointment Date", default=fields.datetime.now(), tracking=True
    )
    checkup_date = fields.Datetime(string="Checkup Date", required=True, tracking=True)

    appointed_doctor_id = fields.Many2one(
        "hospital.doctor", string="Doctor name", required=True
    )
    prescription_medical_test_ids = fields.Many2many(
        "hospital.medicaltest", "medical_test_ids", string="Medical tests"
    )
    pharmacy = fields.One2many(
        "appointment.pharmacy", "appointment_ids", string="pharmacy"
    )
    validity_status = fields.Selection(
        [
            ("invoice", "Invoice Done"),
            ("tobe", "Invoice"),
        ],
        "Status",
        sort=False,
        readonly=True,
        default="tobe",
    )
    is_invoiced = fields.Boolean(copy=False, default=False)
    no_invoice = fields.Boolean(string="Invoice exempt", default=True)
    consultations_id = fields.Many2one(
        "product.product", "Invoice Service", required=True
    )
    invoice_count = fields.Integer(string="Invoice Count", compute="_get_invoiced")
    invoice_ids = fields.Many2many(
        "account.move", string="Invoices", compute="_get_invoiced", copy=False
    )

    def _get_invoiced(self):
        # The invoice_ids are obtained thanks to the invoice lines of the SO
        # lines, and we also search for possible refunds created directly from
        # existing invoices. This is necessary since such a refund is not
        # directly linked to the SO.
        for order in self:
            invoices = order.consultations_id.ids
            order.invoice_ids = invoices
            order.invoice_count = len(invoices)

    def action_view_invoice(self):
        invoices = self.mapped("invoice_ids")
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_move_out_invoice_type"
        )
        if len(invoices) > 1:
            action["domain"] = [("id", "in", invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref("account.view_move_form").id, "form")]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = invoices.id
        else:
            action = {"type": "ir.actions.act_window_close"}

        context = {
            "default_move_type": "out_invoice",
        }
        if len(self) == 1:
            context.update(
                {
                    "default_partner_id": self.patient_id.id,
                    "default_invoice_payment_term_id": False,
                    "default_invoice_origin": self.name,
                    "default_user_id": self.consultations_id.id,
                    "default_invoice_date": date.today(),
                }
            )
        action["context"] = context
        return action
   
    def create_invoice(self):
        lab_req_obj = self.env["hospital.appointment"]
        account_invoice_obj = self.env["account.invoice"]
        account_invoice_line_obj = self.env["account.invoice.line"]

        lab_req = lab_req_obj
        if lab_req.is_invoiced == True:
            raise UserError(_(" Invoice is Already Exist"))
        if lab_req.no_invoice == False:
            res = account_invoice_obj.create(
                {
                    "partner_id": lab_req.patient_id,
                    "date_invoice": date.today(),
                    "account_id": lab_req.patient_id.patient_id.property_account_receivable_id.id,
                }
            )

            res1 = account_invoice_line_obj.create(
                {
                    "product_id": lab_req.consultations_id.id,
                    "product_uom": lab_req.consultations_id.uom_id.id,
                    "name": lab_req.consultations_id.name,
                    "product_uom_qty": 1,
                    "price_unit": lab_req.consultations_id.lst_price,
                    "account_id": lab_req.patient_id.patient_id.property_account_receivable_id.id,
                    "invoice_id": res.id,
                }
            )

            if res:
                lab_req.write({"is_invoiced": True})
                imd = self.env["ir.model.data"]
                action = self.env.ref("account.action_invoice_tree1")
                list_view_id = imd.sudo()._xmlid_to_res_id("account.view_order_form")
                result = {
                    "name": action.name,
                    "help": action.help,
                    "type": action.type,
                    "views": [[list_view_id, "form"]],
                    "target": action.target,
                    "context": action.context,
                    "res_model": action.res_model,
                    "res_id": res.id,
                }
                if res:
                    result["domain"] = "[('id','=',%s)]" % res.id
        else:
            raise UserError(_(" The Appointment is invoice exempt"))
        return result.action_view_invoice()
        return {"type": "ir.actions.act_window_close"}

    # ORM Name Search Method
    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if name:
            args += [
                "|",
                "|",
                ("name", operator, name),
                ("email", operator, name),
                ("name_seq", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return super(HospitalAppointment, self)._name_search(
            name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )

    # Action to send an email
    def action_send_email(self):
        mail_template = self.env.ref("hospital_management.email_template_appointment")
        mail_template.send_mail(self.id, force_send=True)

    # Sequence Generating
    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "hospital.appointment"
            ) or _("New")

        res = super(HospitalAppointment, self).create(vals)
        return res

    # ORM Browse Method
    @api.onchange("inpatient_registration_id")
    def onchange_patient(self):
        if not self.inpatient_registration_id:
            self.patient_id = ""
        inpatient_obj = self.env["hospital.inpatients"].browse(
            self.inpatient_registration_id.id
        )
        self.patient_id = inpatient_obj.id

    # Action for the smart button to view Doctor Details
    def get_doctors(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Details",
            "view_mode": "tree,form",
            "res_model": "hospital.doctor",
            "domain": [("id", "in", self.appointed_doctor_id.ids)],
            "context": "{'create': False}",
        }

    # Date Validation 
    @api.constrains("appointment_date", "checkup_date")
    def _check_date_validation(self):
        for record in self:
            if record.checkup_date < record.appointment_date:
                raise ValidationError("Checkup date should not be previous date.")

    # Changing the status
    def action_status_draft(self):
        self.status = "draft"

    def action_status_confirm(self):
        self.status = "confirm"

    def action_status_done(self):
        self.status = "done"

    def action_status_cancel(self):
        self.status = "cancel"
    
    @api.onchange("patient_id")
    def _change_appointment_note(self):
        if self.patient_id:
            if not self.note:
                self.note = "New appointment"
        else:
            self.note = ""

    # Notification On the Appointment Confirmation
    def sticky_notification(self):
        action = self.env.ref("hospital_management.appointment_action")
        notification = {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": ("Your Appointment is Confirmed"),
                "message": "%s",
                "links": [
                    {
                        "label": self.patient_id.name,
                        "url": f"#action={action.id}&id={self.patient_id.name}&model=hospital.appointment",
                    }
                ],
            },
        }
        return notification

    # Cron job 
    @api.model
    def test_cron_job(self):
        todays_date = datetime.today().date()
        print("Today's Date", todays_date)
        today_month = todays_date.month
        print("Month", today_month)
        today_day = todays_date.day
        check_date = self.env["hospital.appointment"].search([])
        for patients_val in check_date:
            if (
                patients_val.checkup_date.month == today_month
                and patients_val.checkup_date.day == today_day
            ):
                print("Checkup Date")
                print("Today Is Your Checkup Date", patients_val.patient_id.name)
                mail_template = self.env.ref(
                    "hospital_management.email_template_appointment"
                )
                mail_template.send_mail(self.id, force_send=True)
                message = ("Alert Today is your Checkup Date %s") % (
                    patients_val.patient_id.name
                )
                channel_id = self.env.ref("mail.channel_all_employees").id
                channel = self.env["mail.channel"].browse(channel_id)
                channel.message_post(
                    body=(message),
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )

    # That is for DELETE DATA button use unlink function
    def delete_data(self):
        for rec in self:
            rec.patient_id.unlink()


# Appointment.pharmacy model
class AppointmentPharmacy(models.Model):
    _name = "appointment.pharmacy"
    _description = "hospital appointment Pharmacy"

    product_id = fields.Many2one("product.product", required=True)
    price_unit = fields.Float(string="Price", related="product_id.list_price")
    qty = fields.Integer(string="Quantity", default=1)
    appointment_ids = fields.Many2one("hospital.appointment", string="appointment_ids")
