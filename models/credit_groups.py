# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CreditGroups(models.Model):
    _name = 'credit.groups'
    _description = 'Groups of credits'

    name = fields.Char(string='Group Name', required=True)
    code = fields.Char(string="Code", index=True, required=True)
    sale_channel_id = fields.Many2one('sale.channel', string='Sale Channel', required=True)
    global_credit = fields.Float(string='Global Credit', required=True, store=True)
    available_credit = fields.Float(string='Available Credit', compute='_get_available_credit', readonly=True,
                                    store=True)
    used_credit = fields.Float(string='Used Credit', compute='_get_used_credit', readonly=True, store=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    @api.constrains('code')
    def _check_code(self):
        if '026' in self.code:
            raise ValidationError(_("026 sequence no permitted"))

    _sql_constraints = [
        ("unique_code", "unique(code)", _("Code must be unique")),
    ]

    @api.depends('global_credit', 'used_credit')
    def _get_available_credit(self):
        for group in self:
            group.available_credit = group.global_credit - group.used_credit

    def _get_amount_used(self):
        partners = self.env['res.partner'].search([
            ('credit_group_ids', 'in', [self.id])
        ]).ids
        sales = self.env['sale.order'].search([
            ('state', '=', 'sale'),
            ('sale_channel_id', '=', self.sale_channel_id.id),
            ('partner_id', 'in', partners)
        ])
        moves = self.env['account.move'].search([
            ('payment_state', '=', 'not_paid'),
            ('state', '=', 'posted'),
            ('sale_channel_id', '=', self.sale_channel_id.id),
            ('partner_id', 'in', partners)
        ])
        amount = 0.0
        if sales:
            amount += sales.get_total_credit_channel()
        if moves:
            amount += moves.get_total_inv_credit_channel()

        return amount

    @api.depends('global_credit')
    def _get_used_credit(self):
        for group in self:
            group.used_credit = self._get_amount_used()


