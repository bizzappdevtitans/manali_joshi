from odoo import models, fields, api


class TeacherWizard(models.TransientModel):
    _name = "teacher.wizard"

    def _get_default_teachers(self):
        return self.env["school.teachers"].browse(self.env.context.get("active_ids"))

    name_ids = fields.Many2one(
        "school.teachers", string="Teacher", default=_get_default_teachers
    )
    assign = fields.Char(string="Assigned Class")

    def set_teacher_level(self):
        for record in self:
            if record.name_ids:
                for student in record.name_ids:
                    student.assign = self.assign
