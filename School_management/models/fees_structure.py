from odoo import api, fields, models


class FeesStructure(models.Model):
    _name = "fees.structure"
    _inherit = "school.fees"

    academicf = fields.Integer(default="50000", string="Academic Fees")
    tut = fields.Integer(default="5000", string="Tution Fees")
    can = fields.Integer(default="5000", string="Canteen Fees")
    transpo = fields.Integer(default="10000", string="Transportation Fees")
    totalfees = fields.Integer(
        default="70000", string="Total Fee's", compute="_compute_total"
    )
    standard = fields.Selection(
        [
            ("11", "11th Science"),
            ("12", "12th Science"),
        ]
    )
# compute the total fees
    api.depends("academicf", "tut", "can", "transpo")

    def _compute_total(self):
        for rec in self:
            rec.update(
                {
                    "totalfees": rec.academicf + rec.tut + rec.can + rec.transpo,
                }
            )
