from datetime import datetime
from odoo import fields, models


class PublicHolidays(models.Model):
    _name = "academic.holidays"
    _description = "Public Holidays Dates"

    name = fields.Char("Holiday Name", required=True)
    date = fields.Date("Holiday Date", required=True)
    date_day = fields.Char("Day")
    year = fields.Date("Year")
    variable = fields.Boolean("Date may change")
    Type = fields.Selection(
        [
            ("pub", "National Holiday"),
            ("eve", "School Events"),
        ]
    )
