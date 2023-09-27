from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_channel_id = fields.Many2one('sale.channel', string='Sale Channel', compute='_compute_channel', store=True)

    @api.depends('sale_id')
    def _compute_channel(self):
        for picking in self:
            picking.sale_channel_id = picking.sale_id.sale_channel_id

