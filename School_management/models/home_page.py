from odoo import api, fields, models


class HomePage(models.Model):
    _name = "home.page"
    _description = "School Management system"

    home = fields.Html("Gallery")
