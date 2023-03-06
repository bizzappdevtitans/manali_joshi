from odoo import api, fields, models


class SchoolTimetable(models.Model):
    _name = "school.timetable"
    _description = "School Management system"
    _rec_name = "acayear"

    Section = fields.Selection(
        [
            ("pri", "Science"),
            ("sec", "Commerce"),
        ]
    )
    datet = fields.Date(string="Date")
    acayear = fields.Char(string="Year")
    standard = fields.Selection(
        [
            ("11", "11th Science"),
            ("12", "12th Science"),
            ("11c", "11th Commerce"),
            ("12c", "12th Commerce"),
        ]
    )
    timet_ids = fields.Many2many("timetable.structure", string="TimeTable Details")

    # DEFAULT VALUE For field academic year
    @api.model
    def default_get(self, fields_list=[]):
        result = super(SchoolTimetable, self).default_get(fields_list)
        result["acayear"] = "ACA2023"
        return result
