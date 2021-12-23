{
    'name': "Socias",
    'version': '1.0',
    'depends': ['base'],
    "auto_install": True,
    'author': "SeRv_128",
    'category': 'App',
    'description': """
    Módulo para socias o clientas del gimnasio Sevilla Trainers.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/usuario_socia_view.xml',
        'views/res_user_view.xml',
        'views/usuario_socia_menu.xml'
        ],
    "license":"LGPL-3",
}