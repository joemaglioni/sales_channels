#-*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SalesChannels(models.Model):
    _name = 'sale.channel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'sales channels'

    name = fields.Char(string='Channel Name', required=True, track_visibility='always')
    code = fields.Char(string="Client Code", index=True, readonly=True)
    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        string="Warehouse",
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal', domain=[('type', '=', 'sale')], required=True,
    )

    _sql_constraints = [
        ("unique_code", "unique(code)", _("Code must be unique")),
    ]

    @api.model
    def _add_channel_code_reference(self):
        sequence_model = self.env["ir.sequence"]
        seq = sequence_model.next_by_code("sale.channel.code.sequence")
        self.write({
            'code': seq
        })
