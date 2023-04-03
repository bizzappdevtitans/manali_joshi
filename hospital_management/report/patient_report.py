from odoo import api, models


class PatientReport(models.AbstractModel):
    _name = 'report_patient.hospital_management.report_patient_card'
    _description = 'Patient Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hospital.patient'].browse(docids[0])
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', docids[0])])
        vaccinations = self.env['hospital.vaccination'].search([('medical_patient_vaccines_id', '=', docids[0])])
        appointment_list = []
        for app in appointments:
            vals = {
                'name': app.name,
                'note': app.note,
                'date': app.date,
                'patient_id': app.patient_id,
                'age': app.age
            }
        for app in vaccinations:
            vals = {
                'vaccine_product_id': app.vaccine_product_id,
                'next_dose_date': app.next_dose_date,
                'date': app.date,
                'medical_patient_vaccines_id': app.medical_patient_vaccines_id,
                'observations': app.observations
            }
            appointment_list.append(vals)
        print("appointments", appointments)
        print("vaccinations", vaccinations)
        print("appointment_list", appointment_list)
        return {
            'doc_model': 'hospital.patient',
            'docs': docs,
            'appointment_list': appointment_list,
        }