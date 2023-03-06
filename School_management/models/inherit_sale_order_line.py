from odoo import fields, models

class SchoolDescrip(models.Model):
    _inherit = "sale.order.line"

    saleline = fields.Integer(string="Number")

    """ This method is used to pass the value from SO to Project"""

    def _timesheet_create_project_prepare_values(self):
        vals = super(SchoolDescrip, self)._timesheet_create_project_prepare_values()
        vals["project_desc"] = self.order_id.project_desc
        return vals

    """ This method is used to pass the value from SO to Task"""

    def _timesheet_create_task_prepare_values(self, project):
        values = super(SchoolDescrip, self)._timesheet_create_task_prepare_values(project)
        values["project_desc"] = self.order_id.project_desc
        return values
