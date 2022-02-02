from odoo import api, fields, models, exceptions
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class UsuarioSocia(models.Model):#retocar el security 
    _name = "usuario.socia"
    _description = "Usuario de socias o clientas para el gimnasio."
    _order = "name"

    #Atributos de una socia o clienta------------------------------------------------------------------------------------------------------
    tiene_dni = fields.Boolean(default=True)
    dni = fields.Char()
    nie = fields.Char()
    name = fields.Char(required=True)
    surnames = fields.Char(required=True)
    birth_date = fields.Date(required=True)
    peso_actual = fields.Float(required=True)
    altura_actual = fields.Float(required=True)
    dada_alta = fields.Boolean(default=True)
    fecha_de_alta = fields.Date(default=datetime.date.today())
    fecha_de_baja = fields.Date()
    telefono = fields.Char(related="user_id.phone")
    correo = fields.Char(related="user_id.email")
    direccion = fields.Char()
    formas_de_pago = fields.Selection(
        required = True,
        string = 'Tipo de pago',
        selection=[('transferencia', 'Transferencia'), ('en_mano','En Mano')],
        default = "transferencia"
    )
    pagado = fields.Boolean(default=True)#intentar hacer que cuando se pase el dia_de_pago que se ponga a false
    dia_de_pago = fields.Date(default=datetime.date.today() + relativedelta(months=1), readonly=True)#poner automático a 1 mes después cada vez que se paga
    objetivo = fields.Char()
    image_1920 = fields.Image(compute_sudo=True)

    #Relaciones con otras tablas----------------------------------------------------------------------------------------------------------
    user_id = fields.Many2one('res.users', 'User', index=True, store=True, readonly=False)#validar que un usuario no puede repetirse en la base de datos
    revision_mensual_ids = fields.One2many("revision.mensual", "usuario_socia_id", string="Revisión Mensual")
    entrenamientos_socia_ids = fields.One2many("entrenamiento.socia", "usuario_socia_id", string="Entrenamientos")

    #Computed fields----------------------------------------------------------------------------------------------------------------------
    edad = fields.Integer(compute="_compute_edad")
    tipo_pase_temporada = fields.Selection(
        string = 'Tipo de pase de la socia',
        selection=[('estudiante', 'Estudiante'), ('normal','Normal'), ('tercera_edad','Tercera Edad'), ('ninguno','Ninguno')],
        compute = "_compute_tipo_de_pase_segun_edad",
        store=True
    )
    coste_pase = fields.Float(compute="_compute_coste_tipo_pase")


    #Constraints---------------------------------------------------------------------------------------------------------------------------
    _sql_constraints = [
        ('check_peso_actual', 'CHECK(peso_actual > 0)', 'El peso debe ser positivo y mayor que 0.'),
        ('check_altura_actual', 'CHECK(altura_actual > 0)', 'La altura debe ser positiva y mayor que 0.'),
        ('user_uniq', 'unique (user_id)', "Este usuario ya pertenece a otra persona. Por favor, escriba otro distinto."),
        ('dni_uniq', 'unique (dni)', "Ese DNI ya pertenece a alguien."),
        ('nie_uniq', 'unique (nie)', "Ese NIE ya pertenece a alguien."),
        ('unique_email', 'unique (correo)', 'El correo ya existe.'),
    ]


    @api.constrains("birth_date")
    def _check_birth_date(self):
        for record in self:
            fecha_nac = record.birth_date
            hoy = datetime.date.today()

            if fecha_nac > hoy:
                raise ValidationError("La fecha de nacimiento debe ser anterior a la fecha de hoy")


    @api.constrains("name")
    def _check_name(self):
        for record in self:
            name = record.name

            trozos_nombre = name.split(" ")
            for trozo in trozos_nombre:
                primera = True
                if trozo[0] != trozo[0].upper():
                    raise ValidationError("El nombre debe empezar por mayúsculas.")

                for letra in trozo:
                    if re.match("[0-9]", letra):
                        raise ValidationError("El nombre no deben contener números.")
            
                    if letra == letra.upper():
                        if (not primera):
                            raise ValidationError("El nombre debe tener solo la primera letra en mayúsculas.")
                    primera = False
                

    @api.constrains("surnames")
    def _check_surnames(self):
        for record in self:
            apellidos = record.surnames

            trozos_apellidos = apellidos.split(" ")
            for trozo in trozos_apellidos:
                primera = True
                if trozo[0] != trozo[0].upper():
                    raise ValidationError("Los apellidos deben empezar por mayúsculas.")

                for letra in trozo:
                    if re.match("[0-9]", letra):
                        raise ValidationError("Los apellidos no deben contener números.")
            
                    if letra == letra.upper():
                        if (not primera):
                            raise ValidationError("Los apellidos deben tener solo la primera letra en mayúsculas.")
                    primera = False


    @api.constrains("user_id")
    def _check_user_id(self):
        for record in self:
            usuario = record.user_id

            if usuario:

                self._cr.execute('select count(*) from hr_employee where user_id = %s', (usuario.id,))
                data = self._cr.dictfetchall()

                if data[0]['count'] > 0:
                    raise ValidationError("Este usuario ya pertenece a otra persona. Por favor, escriba otro distinto.")



    #Computed fields functions-------------------------------------------------------------------------------------------------------------
    @api.depends("birth_date", "edad")
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
                    if hoy.day >= fecha_nacimiento.day:
                        record.edad = hoy.year - fecha_nacimiento.year

                    else:
                        record.edad = hoy.year - fecha_nacimiento.year -1
                
                if record.edad < 14:
                        raise ValidationError("Para registrarse debe ser mayor de 14 años.")


            else:
                record.edad = 0

            if record.edad < 0:
                record.edad = 0



    @api.depends("edad")
    def _compute_tipo_de_pase_segun_edad(self):
        for record in self:
            edad = record.edad

            if edad > 0:
                if edad <= 21:
                    record.tipo_pase_temporada = "estudiante"

                elif edad <= 59:
                    record.tipo_pase_temporada = "normal"

                else:
                    record.tipo_pase_temporada = "tercera_edad"

            else:
                record.tipo_pase_temporada = "ninguno"



    @api.depends("tipo_pase_temporada", "formas_de_pago")
    def _compute_coste_tipo_pase(self):
        for record in self:
            tipo_pase = record.tipo_pase_temporada
            forma_pago = record.formas_de_pago
            en_mano = forma_pago == "en_mano"

            if tipo_pase: 

                if tipo_pase == "estudiante":
                    if en_mano:
                        record.coste_pase = 20.99
                    else:
                        record.coste_pase = 23.99

                elif tipo_pase == "normal":
                    if en_mano:
                        record.coste_pase = 30.99
                    else:
                        record.coste_pase = 33.99

                elif tipo_pase == "tercera_edad":
                    if en_mano:
                        record.coste_pase = 24.99
                    else:
                        record.coste_pase = 27.99
                
                else:
                    record.coste_pase = 0.0
            
            else:
                record.coste_pase = 0.0


    #Actions-------------------------------------------------------------------------------------------------------------

    def action_dar_de_alta(self):
        for record in self:
            if record.dada_alta == True:
                raise exceptions.UserError("Ya está dada de alta")
            else:
                record.dada_alta = True
                record.fecha_de_alta = datetime.date.today()
                record.fecha_de_baja = None
        return True

    def action_dar_de_baja(self):
        for record in self:
            if record.dada_alta == False:
                raise exceptions.UserError("Ya está dada de baja")
            else:
                record.dada_alta = False
                record.fecha_de_baja = datetime.date.today()
        return True

    



