from odoo import fields, models

class ProjectDescrip(models.Model):
    _inherit = "project.project"

    project_desc = fields.Char(string="Project Description")
    

class ProjectTaskDesc(models.Model):
    _inherit = "project.task"

    project_desc = fields.Char(string="Project Description")
