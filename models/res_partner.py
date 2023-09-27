
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    credit_control = fields.Boolean(string='Credit Control')

    credit_group_ids = fields.Many2many(
        'credit.groups', string='Credits Groups')




    # @api.onchange('credit_group_ids')
    # def _channel_control(self):
    #     import wdb
    #     wdb.set_trace()
    #     a = ""
    #
    #     return True
