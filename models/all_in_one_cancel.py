from odoo import api, models, tools, _, fields
from odoo.exceptions import UserError
from odoo.tests import Form
from odoo.tools import float_is_zero, float_compare, relativedelta, float_round, timedelta


class AllInOneCancel(models.Model):
    _inherit = 'stock.picking'

    def action_cancel(self):
        self.move_line_ids_without_package.state = 'cancel'
        self.move_line_ids_without_package.qty_done = 0
        return self.write({'state': 'cancel'})

    def button_draft(self):
        return self.write({'state': 'draft'})


class PurchaseOrderCancel(models.Model):
    _inherit = 'purchase.order'

    def button_cancel(self):
        return self.write({'state': 'cancel'})


class AccountCancel(models.Model):
    _inherit = 'account.move'

    def button_cancel(self):
        return self.write({'state': 'cancel'})

    def unlink(self):
        for move in self:
            move.line_ids.unlink()


