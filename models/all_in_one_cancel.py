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
        pick = self.env['stock.picking'].search([('origin', '=', self.name)])
        pick.move_line_ids_without_package.state = 'cancel'
        pick.move_line_ids_without_package.qty_done = 0
        pick.write({'state': 'cancel'})
        pick.unlink()
        account = self.env['account.move'].search([('invoice_line_ids.name', 'like', self.name)])
        account.write({'state': 'cancel'})
        account.unlink()
        return self.write({'state': 'cancel'})


class AccountCancel(models.Model):
    _inherit = 'account.move'

    def button_cancel(self):
        self.unlink()
        return self.write({'state': 'cancel'})

    def unlink(self):
        for move in self:
            move.line_ids.unlink()


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    def _compute_supplier_invoice_count(self):
        # retrieve all children partners and prefetch 'parent_id' on them
        all_partners = self.search([('id', 'child_of', self.ids)])
        all_partners.read(['parent_id'])

        supplier_invoice_groups = self.env['account.move'].read_group(
            domain=[('partner_id', 'in', all_partners.ids),
                    ('type', 'in', ('in_invoice', 'in_refund')),
                    ('state', '!=', 'cancel')],
            fields=['partner_id'], groupby=['partner_id']
        )
        partners = self.browse()
        for group in supplier_invoice_groups:
            partner = self.browse(group['partner_id'][0])
            while partner:
                if partner in self:
                    partner.supplier_invoice_count += group['partner_id_count']
                    partners |= partner
                partner = partner.parent_id
        (self - partners).supplier_invoice_count = 0


