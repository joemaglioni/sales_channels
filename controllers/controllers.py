#-*- coding: utf-8 -*-
from odoo import http
import json




class SalesChannels(http.Controller):

    @http.route('/sales_channels', type='json', auth='public', csrf=False)
    def import_groups(self, **kw):
        data = json.loads(http.request.httprequest.data)
        groups = data.get('grupo_credito')
        for group in groups:
            group_obj = http.request.env['credit.groups'].search([
                ('code','=', group['codigo'])
            ])
            channel_obj = http.request.env['sale.channel'].search([
                ('code', '=', group['canal'])
            ])
            if not channel_obj:
                msg = 'No se encontro el canal %s' % group['canal']
                res = self._prepare_vals(404,msg)
                return res

            vals = {
                'name': group['name'],
                'sale_channel_id': channel_obj.id,
                'global_credit': group['credito_global'],
            }
            if group_obj:
                group_obj.update(vals)
            else:
                vals['code'] = group['codigo']
                http.request.env['credit.groups'].create(vals)
        res = self._prepare_vals(200, 'ok')
        return res


    def _prepare_vals(self, code, message):
        return {
            'code': code,
            'message': message
        }

#     @http.route('/sales_channels/sales_channels/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_channels.listing', {
#             'root': '/sales_channels/sales_channels',
#             'objects': http.request.env['sales_channels.sales_channels'].search([]),
#         })

#     @http.route('/sales_channels/sales_channels/objects/<model("sales_channels.sales_channels"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_channels.object', {
#             'object': obj
#         })
