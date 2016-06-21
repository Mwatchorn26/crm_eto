# -*- coding: utf-8 -*-
{
    'name': "CRM - Engineer to Order",

    'summary': """
        CRM additions for an Engineered To Order (eto) company
        """,

    'description': """
        Companies providing an Engineered to Order solution use a slightly different approach than the default sales 
        and manufacturing solutions provided by the base CRM and Manufacturing modules.
        The purpose of this module is to augment the CRM module as needed by salesteams working for an ETO company.
    """,

    'author': "Transformix Engineering Inc.",
    'website': "http://www.transformix.com",

    # Categories can be used to filter modules in modules listing
    # Check <odoo>/addons/base/module/module_data.xml of the full list
    'category': 'Customer Relationship Management',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm'],
    'data': [
             "views/cust_tree_view.xml",
             "views/oppor_menu_view.xml",
             "views/oppor_tree_view.xml",
             "views/oppor_form_view.xml",
             "views/crm_lead_view.xml",
             "data/crm_eto_data.xml",
             "security/ir.model.access.csv",
             "report/crm_eto_report_view.xml",
             ],
    'demo': [],
    'tests': [],
}
