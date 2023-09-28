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
            code_channel = "CH"+group['canal']
            channel_obj = http.request.env['sale.channel'].search([
                ('code', '=', code_channel)
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
                group_obj.write(vals)
            else:
                vals['code'] = group['codigo']
                group_obj.create(vals)
        res = self._prepare_vals(200, 'ok')
        return res


    def _prepare_vals(self, code, message):
        return {
            'code': code,
            'message': message
        }

