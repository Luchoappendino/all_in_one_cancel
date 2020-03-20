# -*- coding: utf-8 -*-
{
    'name': 'All In One Cancel',
    'author': 'Planet_Odoo',
    'version': '13.0.0.0.0',
    'summary ': 'This module will help the user cancel Sale order, Purchase Order,'
                'Shipment and Invoice even after the order is in done state. It will '
                'also reset the inventory to the previous stock values.',
    'company': 'Planet_Odoo',
    'maintainer': 'Planet_Odoo',
    'website': 'www.planet-odoo.com',
    'category': 'Tools',
    'sequence': '121',
    'description': 'This module will help the user cancel Sale order, Purchase Order,'
                'Shipment and Invoice even after the order is in done state. It will '
                'also reset the inventory to the previous stock values.',
    'depends': ['base', 'web', 'mail', 'sale', 'product', 'account', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/all_in_one_cancel_view.xml'

    ],
    'installable': True,
    'auto_install': False
}