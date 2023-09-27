from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_channel_id = fields.Many2one('sale.channel',
                                       string='Sale Channel',
                                       required=True
                                       )
    credit = fields.Selection([
        ('unlimited_credit', 'Unlimited Credit'),
        ('available_credit', 'Available Credit'),
        ('credit_blocked', 'Credit blocked')],
        'Credit', readonly=True)

    @api.onchange('sale_channel_id', 'partner_id', 'tax_totals_json')
    def _check_limite_credit(self):
        for sale in self:
            sale.credit = sale.check_credit()

    def check_credit(self):
        if self.sale_channel_id and self.partner_id:
            groups = self.env['credit.groups'].search([
                ('id','in', self.partner_id.credit_group_ids.ids),
                ('sale_channel_id', '=', self.sale_channel_id.id)
            ])
            if groups:
                filter_group = groups.filtered(lambda group: group.available_credit >= self.amount_total)
                if filter_group:
                    return 'available_credit'
                else:
                    return 'credit_blocked'
            else:
                return 'unlimited_credit'
        return 'unlimited_credit'


    def get_total_credit_channel(self):
        amount = 0
        for sale in self:
            amount += sale.amount_total
        return amount

    @api.onchange('sale_channel_id')
    def _onchange_channel(self):
        if self.sale_channel_id.warehouse_id:
            self.warehouse_id = self.sale_channel_id.warehouse_id.id


    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if self.sale_channel_id.journal_id:
            invoice_vals['journal_id'] = self.sale_channel_id.journal_id.id
            invoice_vals['sale_channel_id'] = self.sale_channel_id.id
        return invoice_vals

    def action_confirm(self):
        self.credit = self.check_credit()
        if self.credit == 'credit_blocked':
            raise ValidationError(
                _('Cannot confirm the sale with blocked credit'))
        res = super(SaleOrder, self).action_confirm()
        return res

