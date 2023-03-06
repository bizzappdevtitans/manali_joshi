from odoo import models, fields, api

class StudentWizard(models.TransientModel):
    _name = 'student.wizard'

    def _get_default_students(self):
        return self.env["school.students"].browse(self.env.context.get("active_ids"))

    name_ids = fields.Many2many("school.students", string="Student", default=_get_default_students)
    level = fields.Char(string="Levels")


    def set_student_level(self):
        for record in self:
            if record.name_ids:
                for student in record.name_ids:
                    student.level = self.level
