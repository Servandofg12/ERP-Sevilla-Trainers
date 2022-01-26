from odoo import api, fields, models
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class MaquinasEntrenamiento(models.Model):#retocar el security 
    _name = "maquinas.entrenamiento"
    _description = "Máquinas del gimnasio."
    _order = "name desc"

    #Atributos de una maquina------------------------------------------------------------------------------------------------------
    name = fields.Char()
