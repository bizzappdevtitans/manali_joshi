from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolTeachers(models.Model):
    _name = "school.teachers"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "School Management system"
    _rec_name = "tecname"

    tecname = fields.Char(string="Teacher Name")
    birthdate = fields.Date(string="Date of Birth")
    photo = fields.Binary(string="Upload Image")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ]
    )
    email = fields.Char(string="Teacher Email")
    phone = fields.Char(string="Teacher Phone")
    address = fields.Text(string="Teacher Address")
    qualification = fields.Char(string="Teacher Qualification")
    assign = fields.Char(string="Assigned Class")
    age = fields.Integer(string="Age", compute="_compute_age")
    
    def btn_whatsapp(self):
        message = "BizzAppDev Welcome You"
        wa_api_url="https://api.whatsapp.com/send?phone=%s&text=%s" %(self.phone,message)
        return {"type": "ir.actions.act_url", "target": "new", "url": wa_api_url}

    def action_send_email(self):
        mail_template = self.env.ref("School_management.email_template_teacher")
        mail_template.send_mail(self.id, force_send=True)

    # Calculate the age by the given dob
    api.depends("birthdate")

    def _compute_age(self):
        for res in self:
            today = date.today()
            if res.birthdate:
                res.age = today.year - res.birthdate.year


    def test_teacher_cron_job(self):
        todays_date = datetime.today().date()
        print("Today's Date", todays_date)
        ongoing_month = todays_date.month
        print("Month", ongoing_month)
        today_day = todays_date.day
        dob_tech = self.env["school.teachers"].search([])
        for tearcher_val in dob_tech:
            if tearcher_val.birthdate.month == ongoing_month and tearcher_val.birthdate.day == today_day:
                print("Birthday Teacher")
                print("Happy Birthday", tearcher_val.tecname)
                mail_template = self.env.ref("School_management.email_template_teacher")
                mail_template.send_mail(self.id, force_send=True)
                message = ("Happy Birthday %s") % (tearcher_val.tecname)
                channel_id = self.env.ref("mail.channel_all_employees").id
                channel = self.env["mail.channel"].browse(channel_id)
                channel.message_post(
                   body=(message),
                   message_type="comment",
                   subtype_xmlid="mail.mt_comment",
                    )

    #Phone Validation
    @api.constrains("phone")
    def _check_phone(self):
        for record in self:
            if record.phone and not str(record.phone).isdigit():
                raise ValidationError(("Cannot enter Characters"))
            if len(record.phone) != 10:
                raise ValidationError("Invalid Number")

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if name:
            args += [
                "|",
                "|",
                ("tecname", operator, name),
                ("email", operator, name),
                ("phone", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
