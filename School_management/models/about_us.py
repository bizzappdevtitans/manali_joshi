from odoo import fields, models


class AboutUs(models.Model):

    _name = "about.us"
    _description = "School Management system"

    description = fields.Html("Gallery")
    des = fields.Html("Description")
