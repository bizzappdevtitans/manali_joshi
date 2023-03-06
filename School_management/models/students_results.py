from odoo import api, fields, models


class StudentsResult(models.Model):
    _name = "students.results"
    _description = "School Management system"

    name_id = fields.Many2one("school.students", "Name")
    stui_id = fields.Char(related="name_id.stui_id", string="Student ID ")
    english = fields.Integer(string="English Score")
    maths = fields.Integer(string="Maths Score")
    comp = fields.Integer(string="Computer Score")
    physics = fields.Integer(string="Physics Score")
    chem = fields.Integer(string="Chemistry Score")
    bio = fields.Integer(string="Biology Score")
    totalmarks = fields.Integer(string="Total", compute="_compute_total")
    percent = fields.Float(string="Percentage", compute="_compute_percentage")
    eligible = fields.Boolean(string="Click if Eligible")
    remarks = fields.Char(string="Remarks")
    

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
                    "percent": rec.totalmarks / 600,
                }
            )

# ORM GETNAME for eligible
    @api.model
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s" % (rec.eligible)))
        return res
