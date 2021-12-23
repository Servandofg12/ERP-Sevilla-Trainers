from odoo import api, fields, models


class Users(models.Model):
    _inherit = 'res.users'

    socia_ids = fields.One2many("usuario.socia", "user_id", string="Datos Socia")

