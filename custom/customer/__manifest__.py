{
    'name': "Customer",
    'version': '1.0',
    'depends': ['base'],
    "auto_install": True,
    'author': "Servandofg12",
    'category': 'App',
    'description': """
    Module for customers from Sevilla Trainers gym.
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizards/customer_monthly_payment.xml',
        'views/customer_view.xml',
        'views/res_user_view.xml',
        'views/monthly_review_view.xml',
        'views/training_machine_views.xml',
        'views/customer_training_views.xml',
        'views/customer_entry_exit_views.xml',
        'views/customer_season_pass_views.xml',
        'views/customer_menu.xml'
        
        ],
    "license":"LGPL-3",
}