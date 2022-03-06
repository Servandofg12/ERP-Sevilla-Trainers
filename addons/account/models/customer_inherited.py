from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class CustomerInherited(models.Model):
    _inherit = "customer.customer"

    
    account_move_ids = fields.One2many("account.move", "customer_id")
