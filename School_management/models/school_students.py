from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re


class SchoolStudents(models.Model):
    _name = "school.students"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "School Management system"

    standard = fields.Selection(
        [
            ("11s", "11th Science"),
            ("12s", "12th Science"),
            ("11c", "11th Commerce"),
            ("12c", "12th Commerce"),
        ]
    )
    name = fields.Char(string="Students Name",required="1")
    birthdate = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ]
    )
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
    Section = fields.Selection(
        [
            ("pri", "Science"),
            ("sec", "Commerce"),
        ]
    )
    photo = fields.Binary(string="Upload Image")
    level = fields.Char(string="Level")

    result_ids = fields.One2many("students.results", "name_id", "Result")
    Total_count = fields.Integer(compute="compute_count")

    stui_id = fields.Char(
        string="Student Id", required=True, index=True, copy=False, default="New"
    )
    birthday_month = fields.Integer(
        string="Birthday Month",
        compute="_compute_bm",
        store=True,
        index=True,
        readonly=True,
    )

    def action_send_email(self):
        mail_template = self.env.ref("School_management.email_template_student")
        mail_template.send_mail(self.id, force_send=True)

    @api.depends("birthdate")
    def _compute_bm(self):
        for record in self:
            if record.birthdate:
                record.birthday_month = record.birthdate.month
            else:
                record.birthday_month = False

    @api.model
    def test_cron_job(self):
        todays_date = datetime.today().date()
        print("Today's Date", todays_date)
        today_month = todays_date.month
        print("Month", today_month)
        today_day = todays_date.day
        dob = self.env["school.students"].search([])
        for students_val in dob:
            if students_val.birthdate.month == today_month and students_val.birthdate.day == today_day:
                print("Birthday Students")
                print("Happy Birthday", students_val.name)
                mail_template = self.env.ref("School_management.email_template_student")
                mail_template.send_mail(self.id, force_send=True)
                message = ("Happy Birthday %s") % (students_val.name)
                channel_id = self.env.ref("mail.channel_all_employees").id
                channel = self.env["mail.channel"].browse(channel_id)
                channel.message_post(
                   body=(message),
                   message_type="comment",
                   subtype_xmlid="mail.mt_comment",
                    )

    # Calculate the age by the given dob
    api.depends("birthdate")

    def _compute_age(self):
        for res in self:
            today = date.today()
            if res.birthdate:
                res.age = today.year - res.birthdate.year

    def get_vehicles(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Result",
            "view_mode": "tree,form",
            "res_model": "students.results",
            "domain": [("eligible", "=", self.id)],
            "context": "{'create': False}",
        }

    # ORM search count

    def compute_count(self):
        for record in self:
            record.Total_count = self.env["students.results"].search_count(
                [("eligible", "=", self.id)]
            )

    # ORM BROWSE METHOD

    def action_browse(self):
        for rec in self:
            student = self.env["school.students"].browse(32)
            print(student.name)

    # Name search method

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
                ("stui_id", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return super(SchoolStudents, self)._name_search(
            name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )

    # sequence generate for student id
    @api.model
    def create(self, vals):
        vals["stui_id"] = self.env["ir.sequence"].next_by_code("school.students")
        return super(SchoolStudents, self).create(vals)

# phone validation
    @api.constrains("phone")
    def _check_phone(self):
        for values in self:
            if values.phone and not str(values.phone).isdigit():
                raise ValidationError(("Cannot enter Characters"))
            if len(values.phone) != 10:
                raise ValidationError("Invalid Number")