from odoo import fields, models

class DeliveryValue(models.Model):
    _inherit = "stock.move"

    mrp_order = fields.Char(string="Manufacturing")
    pur_order = fields.Char(string="Purchase Order")


    """ This method is used to pass the value from SO to DO"""

    def _get_new_picking_values(self):
        vals = super(DeliveryValue, self)._get_new_picking_values()
        Customer_Type = self.group_id.sale_id.Customer_Type
        vals["Customer_Type"] = (
            any(rule.propagate_carrier for rule in self.rule_id) and Customer_Type
        )
        delivery = self.group_id.sale_id.delivery
        vals["delivery"] = (
            any(rule.propagate_carrier for rule in self.rule_id) and delivery
        )
        return vals

    """ This method is used to pass the value from SO to MO"""

    def _prepare_procurement_values(self):
        res = super()._prepare_procurement_values()
        res['mrp_order'] = self.sale_line_id.order_id.mrp_order
        return res

    # def _prepare_procurement_values(self):
    #     val = super()._prepare_procurement_values()
    #     val['pur_order'] = self.sale_line_id.order_id.pur_order
    #     return val


