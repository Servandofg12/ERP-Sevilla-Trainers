from odoo import api, fields, models
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class RevisionMensual(models.Model):
    _name = "revision.mensual"
    _description = "Revisión mensual para las socias del gimnasio."
    _order = "fecha_realizada desc"

    #Atributos de una socia o clienta------------------------------------------------------------------------------------------------------
    nuevo_peso = fields.Float(required=True)
    nueva_altura = fields.Float(required=True)
    porcentaje_grasa_corporal = fields.Float(required=True)
    indice_masa_corporal = fields.Float(required=True)
    medida_pecho = fields.Float(required=True)
    medida_cintura = fields.Float(required=True)
    medida_abdomen = fields.Float(required=True)
    medida_caderas = fields.Float(required=True)
    medida_muslos = fields.Float(required=True)
    medida_brazos = fields.Float(required=True)
    fecha_realizada = fields.Date(default=datetime.date.today())

    #Relaciones con otras tablas----------------------------------------------------------------------------------------------------------
    usuario_socia_id = fields.Many2one("usuario.socia", string="Socia")


    #Constraints---------------------------------------------------------------------------------------------------------------------------
    _sql_constraints = [
        ('check_nuevo_peso', 'CHECK(nuevo_peso > 0)', 'El peso debe ser positivo y mayor que 0.'),
        ('check_nueva_altura', 'CHECK(nueva_altura > 0)', 'La altura debe ser positiva y mayor que 0.'),
        ('check_porcentaje_grasa_corporal', 'CHECK(porcentaje_grasa_corporal > 0)', 'El porcentaje de grasa debe ser positiva y mayor que 0.'),
        ('check_indice_masa_corporal', 'CHECK(indice_masa_corporal > 0)', 'El indice de masa corporal debe ser positiva y mayor que 0.'),
        ('check_medida_pecho', 'CHECK(medida_pecho > 0)', 'La medida de pecho debe ser positiva y mayor que 0.'),
        ('check_medida_cintura', 'CHECK(medida_cintura > 0)', 'La medida de cintura debe ser positiva y mayor que 0.'),
        ('check_medida_abdomen', 'CHECK(medida_abdomen > 0)', 'La medida de abdomen debe ser positiva y mayor que 0.'),
        ('check_medida_caderas', 'CHECK(medida_caderas > 0)', 'La medida de caderas debe ser positiva y mayor que 0.'),
        ('check_medida_muslos', 'CHECK(medida_muslos > 0)', 'La medida de muslos debe ser positiva y mayor que 0.'),
        ('check_medida_brazos', 'CHECK(medida_brazos > 0)', 'La medida de brazos debe ser positiva y mayor que 0.'),
    ]


    #On create ---------------------------------------------------------------------------------------------------------------------------
    @api.model
    def create(self, vals):
        hoy = datetime.date.today()
        hoy_mas_un_mes = hoy + relativedelta(months=1)
        fecha_comparacion = hoy_mas_un_mes - relativedelta(days=1)
        socia = self.env["usuario.socia"].browse(vals['usuario_socia_id'])

        if len(socia.revision_mensual_ids)>0:
            fecha_ultima_revision = socia.revision_mensual_ids[-1].fecha_realizada
        else:
            fecha_ultima_revision = hoy + relativedelta(months=2)

        if fecha_ultima_revision < fecha_comparacion:
            raise UserError("Todavia no puede hacerse su revisión. Debe esperar hasta el día " + str(fecha_ultima_revision + relativedelta(months=1)))
        else:
        
            #Editamos los datos de la socia y actualizamos el peso actual y la altura actual con la de la revision mensual
            self.env["usuario.socia"].browse(vals['usuario_socia_id']).write(
                    {
                        "peso_actual": vals['nuevo_peso'],
                        "altura_actual": vals['nueva_altura']
                    }
                )
            
            #Creamos la revision mensual
            result = super(RevisionMensual, self).create(vals)
            return result