from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentsResult(models.Model):
    _name = "students.results"
    _description = "School Management system"

    name_id = fields.Many2one("school.students", "Name")
    stui_id = fields.Char(related="name_id.stui_id", string="Student ID ")
    english = fields.Float(string="English Score")
    maths = fields.Float(string="Maths Score")
    comp = fields.Float(string="Computer Score")
    physics = fields.Float(string="Physics Score")
    chem = fields.Float(string="Chemistry Score")
    bio = fields.Float(string="Biology Score")
    totalmarks = fields.Float(string="Total", compute="_compute_total")
    percent = fields.Float(string="Percentage", compute="_compute_percentage")
    eligible = fields.Boolean(string="Click if Eligible")
    remarks = fields.Char(string="Remarks")
    
    @api.constrains("english", "maths", "comp", "physics", "chem", "bio")
    def _check_description(self):
        if (
            self.english > 100
            or self.maths > 100
            or self.comp > 100
            or self.physics > 100
            or self.chem > 100
            or self.bio > 100
        ):
            raise ValidationError("Marks can't be grater than 100")

# Compute the total marks of subjects
    api.depends("english", "maths", "comp", "physics", "chem", "bio")

    def _compute_total(self):
        for rec in self:
            rec.update(
                {
                    "totalmarks": rec.english
                    + rec.maths
                    + rec.comp
                    + rec.physics
                    + rec.chem
                    + rec.bio,
                }
            )
# Compute the Percentage 

    def _compute_percentage(self):
        for rec in self:
            rec.update(
                {
                    "percent": rec.totalmarks / 6,
                }
            )

# ORM GETNAME for eligible
    @api.model
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s" % (rec.eligible)))
        return res
