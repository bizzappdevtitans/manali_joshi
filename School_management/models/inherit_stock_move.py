from odoo import fields, models, api


class DeliveryValue(models.Model):
    _inherit = "stock.move"

    mrp_order = fields.Char(string="Manufacturing")
    pur_order = fields.Char(string="Purchase Order")
    weight = fields.Float(string="Weight", compute="get_data")

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

    def get_data(self):
        for move in self:
            if not (move.picking_id and move.picking_id.group_id):
                continue
            picking = move.picking_id
            sale_order = (
                self.env["sale.order"]
                .sudo()
                .search([("procurement_group_id", "=", picking.group_id.id)], limit=1)
            )
            for line in sale_order.order_line:
                if line.product_id.id != move.product_id.id:
                    continue
                move.update({"weight": line.weight})

    # def _get_new_picking_values(self):
    #     vals = super(DeliveryValue, self)._get_new_picking_values()
    #     weight = self.group_id.origin_move_line.weight
    #     vals["weight"] = (
    #         any(rule.propagate_carrier for rule in self.rule_id) and weight
    #     )
    #     return vals

    # def _prepare_procurement_values(self, group_id=False):
    #     res = super(DeliveryValue,self)._prepare_procurement_values(group_id)
    #     res['weight'] = self.sale_line_id.order_id.weight
    #     return res

    """ This method is used to pass the value from SO to MO"""

    def _prepare_procurement_values(self):
        res = super()._prepare_procurement_values()
        res["mrp_order"] = self.sale_line_id.order_id.mrp_order
        return res

    # def _prepare_procurement_values(self):
    #     val = super()._prepare_procurement_values()
    #     val['pur_order'] = self.sale_line_id.order_id.pur_order
    #     return val
