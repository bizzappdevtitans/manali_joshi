from odoo import fields, models

class StockRule(models.Model):
    _inherit = 'stock.rule'


    """ This method is used to pass the value from SO to MO"""

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom):
      vals = super(StockRule, self)._prepare_mo_vals(product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom)
      vals["mrp_order"] = values.get('mrp_order')
      return vals

    # def _prepare_purchase_order(self, company_id, origins, values):
    #     vals = super(StockRule, self)._prepare_purchase_order(company_id,origins,values)
    #     values = values[0]
    #     vals['pur_order'] = values['supplier'].purchase_requisition_id.pur_order
    #     return vals


