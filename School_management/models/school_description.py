from odoo import api, fields, models


class SchoolDescription(models.Model):
    _inherit = "sale.order"

    # decs = fields.Text(string="Query")
    Customer_Type = fields.Selection(
        [
            ("new", "New Customer"),
            ("exi", "Existing Customer"),
        ]
    )
    delivery = fields.Char(string="Delivery Description")
    invoice_id = fields.Char(string="Invoice Description")
    project_desc = fields.Char(string="Project Description")
    pur_order = fields.Char(string="Purchase Order")

    def _prepare_invoice(self):
        invoice_vals = super(SchoolDescription, self)._prepare_invoice()
        invoice_vals["invoice_desc"] = self.invoice_id
        return invoice_vals

    def _prepare_analytic_account_data(self, prefix=None):
        vals = super(SchoolDescription, self)._prepare_analytic_account_data(prefix)
        vals["project_desc"] = self.project_desc
        return vals

    # def _purchase_service_prepare_order_values(self, supplierinfo):
    #     self.ensure_one()
    #     partner_supplier = supplierinfo.name
    #     pur_vals = super(SchoolDescription, self)._purchase_service_prepare_order_values(supplierinfo)
    #     pur_vals["pur_order"] = partner_supplier.pur_order
    #     return pur_vals

class InvoiceDown(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    # both methods works

    # def _prepare_invoice_values(self, order, name, amount, so_line):
    #     invoice_vals = super(InvoiceDown, self)._prepare_invoice_values(order, name, amount, so_line)
    #     invoice_vals["invoice_desc"] = order.invoice_id
    #     return invoice_vals

    def _create_invoice(self, order, so_line, amount):
        invoice_vals = super(InvoiceDown, self)._create_invoice(order, so_line, amount)
        invoice_vals["invoice_desc"] = order.invoice_id
        return invoice_vals


class SaleDelivery(models.Model):
    _inherit = "stock.picking"
    delivery = fields.Char(string="Delivery Description")
    Customer_Type = fields.Selection(
        [
            ("new", "New Customer"),
            ("exi", "Existing Customer"),
        ]
    )

class DeliveryValue(models.Model):
    _inherit = "stock.move"

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

    def _prepare_procurement_values(self):
        proc_values = super(DeliveryValue,self)._prepare_procurement_values()
        if self.restrict_partner_id:
            proc_values['pur_order'] = self.restrict_partner_id
            self.restrict_partner_id = False
        return proc_values


class SaleInvoice(models.Model):
    _inherit = "account.move"

    invoice_desc = fields.Char(string="Invoice Description")


class SchoolDescrip(models.Model):
    _inherit = "sale.order.line"

    saleline = fields.Integer(string="Number")


class ProjectDescrip(models.Model):
    _inherit = "project.project"

    project_desc = fields.Char(
        string="Project Description", related="analytic_account_id.project_desc"
    )


class accountanalytic(models.Model):
    _inherit = "account.analytic.account"

    project_desc = fields.Char(string="Project Description")


class ProjectTaskDesc(models.Model):
    _inherit = "project.task"

    project_desc = fields.Char(
        string="Project Description", related="project_id.project_desc"
    )

class PoInherit(models.Model):
    _inherit = "purchase.order"

    pur_order = fields.Char(string="Purchase Order")



# method of so to do but directly
# @api.model
# def action_confirm(self):
#  result = super(SchoolDescription, self).action_confirm()
#  for order in self:
#     order.picking_ids.write({'delivery': order.delivery})
