from odoo import fields, models

class PoInherit(models.Model):
    _inherit = "purchase.order"

    pur_order = fields.Char(string="Purchase Order")

    # def _get_action_view_picking(self, pickings):
    #     vals = super(PoInherit, self)._get_action_view_picking(pickings)
    #     vals['pur_order'] = self.pur_order
    #     return vals

# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
    
#     pur_order = fields.Char(string="Purchase Order")


#     def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, company_id, values, po):
#         res = super()._prepare_purchase_order_line_from_procurement(product_id, product_qty, product_uom, company_id, values, po)
#         res['pur_order'] = values.get('pur_order')
#         return res

    # def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, supplier, po):
    #     vals = super(PurchaseOrderLine, self)._prepare_purchase_order_line(product_id, product_qty, product_uom, company_id, supplier, po)
    #     vals["pur_order"] = self.pur_order
    #     return vals
