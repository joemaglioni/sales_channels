
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    credit_control = fields.Boolean(string='Credit Control')

    credit_group_ids = fields.Many2many(
        'credit.groups', string='Credits Groups')

    def write(self, vals):
        group_ids = vals.get('credit_group_ids')
        if group_ids:
            if group_ids[0][2]:
                groups = self.env['credit.groups'].search([(
                    'id', 'in', group_ids[0][2]
                )])

                for group in groups:
                    group.sale_channel_id._add_channel_code_reference()

        return super(ResPartner, self).write(vals)

