from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class HospitalAppointmentWizard(models.TransientModel):
    _name = 'hospital.appointment.wizard'
    _description = 'Create Appointment'

    name = fields.Char(string='Appointment Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one("hospital.patient", string='Patient Name', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], related='patient_id.gender')
    phone = fields.Char(string='Phone', related='patient_id.phone')
    email = fields.Char(string='Email', related='patient_id.email')
    age = fields.Integer(string='Age', related='patient_id.age')
    appointment_date = fields.Datetime(string='Appointment Date', default=fields.datetime.now())
    checkup_date = fields.Datetime(string='Checkup Date', required=True)
    inpatient_registration_id = fields.Many2one('hospital.inpatients',string="Inpatient Registration")
    urgency_level = fields.Selection([
            ('a', 'Normal'),
            ('b', 'Urgent'),
            ('c', 'Medical Emergency'),
        ], 'Urgency Level', sort=False,default="b")
    patient_status = fields.Selection([
            ('ambulatory', 'Ambulatory'),
            ('outpatient', 'Outpatient'),
            ('inpatient', 'Inpatient'),
        ], 'Patient status', sort=False,default='outpatient')
    appointed_doctor_id = fields.Many2one("hospital.doctor", string="Doctor name", required=True)
    consultations_id = fields.Many2one('product.product','Consultation Service',required=True)

    def get_doctors(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Details",
            "view_mode": "tree,form",
            "res_model": "hospital.doctor",
            "domain": [("id", "in", self.appointed_doctor_id.ids)],
            "context": "{'create': False}",
        }
    
    def action_create_patient_appointment(self):
       vals={
           'patient_id': self.patient_id.id,
           'gender': self.gender,
           'phone': self.phone,
           'email': self.email,
           'age': self.age,
           'appointment_date': self.appointment_date,
           'checkup_date': self.checkup_date,
           'appointed_doctor_id': self.appointed_doctor_id.id,
           'consultations_id':self.consultations_id.id


       }
       appointment_id=self.env['hospital.appointment'].create(vals)
       return {
           'name':_('Appointment'),
           'type':'ir.actions.act_window',
           'view_mode':'form',
           'res_model':'hospital.appointment',
           'res_id':appointment_id.id,
           'target':'new',
       }

    @api.constrains('appointment_date', 'checkup_date')
    def _check_date_validation(self):
        for record in self:
            if record.checkup_date < record.appointment_date:
                raise ValidationError('Checkup date should not be previous date.')

    # That is fOR DELETE DATA button use unlink function
    def delete_data(self):
        for rec in self:
            rec.patient_id.unlink()