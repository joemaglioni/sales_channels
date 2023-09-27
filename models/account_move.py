from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_channel_id = fields.Many2one('sale.channel', string='Sale Channel')


    def get_total_inv_credit_channel(self):
        amount = 0
        for invoice in self:
            amount += invoice.tax_totals_json
        return amount
