# -*- coding: utf-8 -*-
{
    'name': "sales_channels",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'account',
                'sale',
                'stock'
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_channel_views.xml',
        'views/sale_order_views.xml',
        'views/credit_groups_views.xml',
        'views/res_partner_views.xml',
        'views/templates.xml',
        'data/ir_sequence_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
