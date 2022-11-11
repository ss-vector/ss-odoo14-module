# -*- coding: utf-8 -*-
{
    'name': "s.Control Tienda",

    'summary': """
        Main accounts and cash control module""",

    'description': """
        Control cash and organize workflows so it can help local accountability
    """,

    'author': "@ss-vector",
    'website': "http://www.eltriunfo.pe",

    # Open source license
    'license': "LGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'base'],

    # always loaded
    'data': [
        # security
        'security/ir.model.access.csv',
        # data files
        'data/data.xml',
        'views/views.xml',
        'views/operations.xml',
        'views/closure.xml'
        # report
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    # installable, application, auto_install = "False"
    'installable': True,
    'application': True,
    'auto_install': False,
}
