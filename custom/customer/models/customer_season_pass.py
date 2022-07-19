from odoo import api, fields, models, exceptions, Command
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CustomerSeasonPass(models.Model):
    _name = "customer.season.pass"
    _description = "Season pass for the Sevilla Trainers gym's Customers."
    _order = "name"

    #Atributes ------------------------------------------------------------------------------------------------------
    name = fields.Char(required=True)
    until_age = fields.Integer(required=True)
    cost = fields.Float(required=True)


    #Relations between tables----------------------------------------------------------------------------------------
    customer_ids = fields.One2many("customer.customer", "customer_season_pass_id", string="Customer Season Pass")
