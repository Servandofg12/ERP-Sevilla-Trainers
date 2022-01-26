from odoo import api, fields, models
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class EntrenamientoSocia(models.Model):#retocar el security 
    _name = "entrenamiento.socia"
    _description = "Entrenamiento de las socias o clientas del gimnasio."
    _order = "fecha_entreno desc"

    #Atributos de un entrenamiento------------------------------------------------------------------------------------------------------
    fecha_entreno = fields.Date(default=datetime.date.today())
    nombre = fields.Char()
    num_vueltas = fields.Integer(default=1)
    usa_maquinas = fields.Boolean()
    maquinas_entrenamiento_ids = fields.Many2many("maquinas.entrenamiento", string="Máquinas")

    #Relaciones con otras tablas----------------------------------------------------------------------------------------------------------
    usuario_socia_id = fields.Many2one("usuario.socia", string="Socia")
