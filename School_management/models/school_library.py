from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError


class SchoolLibrary(models.Model):
    _name = "school.library"
    _description = "School Management system"

    # name_stu = fields.Many2one("school.students", "Name")
    lib_id = fields.Integer(string="Library ID")
    # phone = fields.Char(related="name_stu.phone", string="Students Phone")
    subject = fields.Text(string="Approval Subject")
    category = fields.Selection(
        [
            ("borrow", "Borrow Books"),
            ("purchase", "Purchase Books"),
            ("read", "Read Books"),
            ("other", "Others"),
        ]
    )
    items = fields.Text(string="Items Name")
    quantity = fields.Integer(string="Quantity")
    period = fields.Char(string="Period")
    time1 = fields.Datetime(string="From")
    time2 = fields.Datetime(string="To")
    references = fields.Reference(
        selection=[
            ("school.students", "Student Profile"),
            ("school.teachers", "Teacher Profile"),
        ],
        string="Details",
    )

    _sql_constraints = [
        ("lib_id_unique", "unique (lib_id)", "Student ID is already exists...!")
    ]

    @api.constrains("category")
    def button_send(self):
        self.ensure_one()
        if not self.category:
            raise UserError("No Category were selected.")
            return True

    # ORM GETNAME
    @api.model
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s" % (rec.lib_id)))
        return res
