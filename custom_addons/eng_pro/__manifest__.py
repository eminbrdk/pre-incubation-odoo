{
    'name': 'Pre-incubation',
    'version': '1.0',
    'category': 'ERP',
    'summary': 'Modul for Pre-Incubation',
    'author': 'Muhammed Emin Bardakcı, Ulaş Kaba & Cumhur Öksüz',
    'depends': ["base"],
    'data': [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/model_access.xml',
        'security/ir_rule.xml',

        "views/pro_application_view.xml", # bu menüden önce yazılmalı çoomelli !!!!!!!!!!!!
        "views/pro_group_project_view.xml",
        "views/menu_items.xml",

        "views/apply_web_view.xml",
        "views/create_user_web_view.xml",
        "views/aplly_success_web_view.xml",
        "views/create_user_success.xml"
    ],
    "demo": [],
    'installable': True,
    'license': 'LGPL-3',
}