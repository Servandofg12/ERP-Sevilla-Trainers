from odoo import api, fields, models, exceptions
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class UsuarioSocia(models.Model):#retocar el security 
    _name = "usuario.socia"
    _description = "Usuario de socias o clientas para el gimnasio"
    _order = "name"

    #Atributos de una socia o clienta------------------------------------------------------------------------------------------------------
    name = fields.Char(required=True)
    surnames = fields.Char(required=True)#validar bien
    birth_date = fields.Date(required=True)#validar bien
    peso_actual = fields.Float(required=True)
    altura_actual = fields.Float(required=True)
    dada_alta = fields.Boolean(default=True)
    fecha_de_alta = fields.Date(default=datetime.date.today())
    fecha_de_baja = fields.Date()

    #Relaciones con otras tablas----------------------------------------------------------------------------------------------------------
    user_id = fields.Many2one('res.users', 'User', index=True, store=True, readonly=False)#validar que un usuario no puede repetirse en la base de datos

    #Computed fields----------------------------------------------------------------------------------------------------------------------
    edad = fields.Integer(compute="_compute_edad")
    tipo_pase_temporada = fields.Selection(
        string = 'Tipo de pase de la socia',
        selection=[('estudiante', 'Estudiante'), ('normal','Normal'), ('tercera_edad','Tercera Edad')],
        compute = "_compute_tipo_de_pase_segun_edad",
        store=True
    )
    coste_pase = fields.Float(compute="_compute_coste_tipo_pase")


    #Constraints---------------------------------------------------------------------------------------------------------------------------
    _sql_constraints = [
        ('check_peso_actual', 'CHECK(peso_actual > 0)', 'El peso debe ser positivo y mayor que 0.'),
        ('check_altura_actual', 'CHECK(altura_actual > 0)', 'La altura debe ser positiva y mayor que 0.'),
        ('user_uniq', 'unique (user_id)', "Un usuario no puede pertenecer a dos socias.")
    ]

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            name = record.name

            if name[0] != name[0].upper():
                raise ValidationError("El nombre debe empezar por mayúsculas.")

            primera = True
            for letra in name:
                if re.match("[0-9]", letra):
                    raise ValidationError("El nombre no debe contener números.")
                
                if letra == letra.upper():
                    if (not primera):
                        raise ValidationError("El nombre debe tener solo la primera letra en mayúsculas.")
                primera = False
                

    @api.constrains("surnames")#queda mejorar esta restriccion
    def _check_surnames(self):
        for record in self:
            apellidos = record.surnames

            trozos_apellidos = apellidos.split(" ")
            primera = True
            for trozo in trozos_apellidos:
                if trozo[0] != trozo[0].upper():
                    raise ValidationError("Los apellidos deben empezar por mayúsculas.")

                if re.match("[0-9]", trozo):
                    raise ValidationError("Los apellidos no deben contener números.")
        
                if trozo == trozo.upper():
                    if (not primera):
                        raise ValidationError("Los apellidos debe tener solo la primera letra en mayúsculas.")
                primera = False


    @api.constrains("user_id")
    def _check_name_and_surnames(self):
        for record in self:
            usuarios = record.user_id.socia_ids
            for usuario in usuarios:
                print(usuario)


    #Computed fields functions-------------------------------------------------------------------------------------------------------------
    @api.depends("birth_date")
    def _compute_edad(self):
        for record in self:
            fecha_nacimiento = record.birth_date
            hoy = datetime.date.today()

            if fecha_nacimiento:

                if hoy.month < fecha_nacimiento.month:
                    record.edad = hoy.year - fecha_nacimiento.year - 1

                elif hoy.month > fecha_nacimiento.month:
                    record.edad = hoy.year - fecha_nacimiento.year

                else:
                    if hoy.day <= fecha_nacimiento.day:
                        record.edad = hoy.year - fecha_nacimiento.year

                    else:
                        record.edad = hoy.year - fecha_nacimiento.year -1
            else:
                record.edad = 0


    @api.depends("edad")
    def _compute_tipo_de_pase_segun_edad(self):
        for record in self:
            edad = record.edad
            record.tipo_pase_temporada = "normal"

            if edad <= 21:
                record.tipo_pase_temporada = "estudiante"

            elif edad <= 59:
                record.tipo_pase_temporada = "normal"

            else:
                record.tipo_pase_temporada = "tercera_edad"



    @api.depends("tipo_pase_temporada")
    def _compute_coste_tipo_pase(self):
        for record in self:
            tipo_pase = record.tipo_pase_temporada

            if tipo_pase:

                if tipo_pase == "estudiante":
                    record.coste_pase = 20.99

                elif tipo_pase == "normal":
                    record.coste_pase = 30.99

                else:
                    record.coste_pase = 24.99
            
            else:
                record.coste_pase = 0.0

    



