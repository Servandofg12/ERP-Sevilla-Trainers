# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import Form
from odoo.addons.hr.tests.common import TestHrCommon
from odoo.tests import tagged
import datetime
from dateutil.relativedelta import relativedelta

@tagged('empleados')
class TestHrEmployee(TestHrCommon):

    def setUp(self):
        super().setUp()
        self.user_without_image = self.env['res.users'].create({
            'name': 'Marc Demo',
            'email': 'mark.brown23@example.com',
            'image_1920': False,
            'login': 'demo_1',
            'password': 'demo_123'
        })
        self.employee_without_image = self.env['hr.employee'].create({
            'user_id': self.user_without_image.id,
            'image_1920': False
        })

        #Para las pruebas de dar de alta y baja
        self.user_without_image_2 = self.env['res.users'].create([{
            'name': 'Prueba',
            'email': 'prueba23@example.com',
            'image_1920': False,
            'login': 'prueba_1',
            'password': 'prueba_123'
        },{
            'name': 'Prueba2',
            'email': 'prueba23333@example.com',
            'image_1920': False,
            'login': 'prueba_2',
            'password': 'prueba_123'
        },{
            'name': 'Prueba3',
            'email': 'prueba3333@example.com',
            'image_1920': False,
            'login': 'prueba_3',
            'password': 'prueba_123'
        }])

        self.employee_without_image_2 = self.env['hr.employee'].create([{
            'user_id': self.user_without_image_2[0].id,
            'image_1920': False,
        },{
            'user_id': self.user_without_image_2[1].id,
            'image_1920': False,
            'dada_alta': False,
            'fecha_de_baja': datetime.date.today() - relativedelta(months=2)
        }])

        fecha_normal = datetime.date.today() - relativedelta(years=23)

        self.socias = self.env['usuario.socia'].create(
                {
                    'tiene_dni': True, 
                    'dni': "66727211S",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_normal,
                    'peso_actual': 65.0,
                    'altura_actual': 1.75,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar confianza en mí misma.",
                    'user_id': self.user_without_image_2[2].id
                }
            )





    def test_employee_resource(self):
        _tz = 'UTC'
        self.res_users_hr_officer.company_id.resource_calendar_id.tz = _tz
        Employee = self.env['hr.employee'].with_user(self.res_users_hr_officer)
        employee_form = Form(Employee)
        employee_form.name = 'Raoul Grosbedon'
        employee_form.work_email = 'raoul@example.com'
        employee = employee_form.save()
        self.assertEqual(employee.tz, _tz)

    def test_employee_from_user(self):
        _tz = 'Pacific/Apia'
        _tz2 = 'America/Tijuana'
        self.res_users_hr_officer.company_id.resource_calendar_id.tz = _tz
        self.res_users_hr_officer.tz = _tz2
        Employee = self.env['hr.employee'].with_user(self.res_users_hr_officer)
        employee_form = Form(Employee)
        employee_form.name = 'Raoul Grosbedon'
        employee_form.work_email = 'raoul@example.com'
        employee_form.user_id = self.res_users_hr_officer
        employee = employee_form.save()
        self.assertEqual(employee.name, 'Raoul Grosbedon')
        self.assertEqual(employee.work_email, self.res_users_hr_officer.email)
        self.assertEqual(employee.tz, self.res_users_hr_officer.tz)

    '''def test_employee_from_user_tz_no_reset(self):
        _tz = 'Pacific/Apia'
        self.res_users_hr_officer.tz = False
        Employee = self.env['hr.employee'].with_user(self.res_users_hr_officer)
        employee_form = Form(Employee)
        employee_form.name = 'Raoul Grosbedon'
        employee_form.work_email = 'raoul@example.com'
        employee_form.tz = _tz
        employee_form.user_id = self.res_users_hr_officer
        employee = employee_form.save()
        self.assertEqual(employee.name, 'Raoul Grosbedon')
        self.assertEqual(employee.work_email, self.res_users_hr_officer.email)
        self.assertEqual(employee.tz, _tz)'''

    def test_employee_has_avatar_even_if_it_has_no_image(self):
        self.assertTrue(self.employee_without_image.avatar_128)
        self.assertTrue(self.employee_without_image.avatar_256)
        self.assertTrue(self.employee_without_image.avatar_512)
        self.assertTrue(self.employee_without_image.avatar_1024)
        self.assertTrue(self.employee_without_image.avatar_1920)

    def test_employee_has_same_avatar_as_corresponding_user(self):
        self.assertEqual(self.employee_without_image.avatar_1920, self.user_without_image.avatar_1920)



    #TESTS PARA COMPROBAR LA FUNCIONALIDAD DE DAR DE ALTA Y BAJA -----------------------------------------------------------------------

    #test para comprobar que se da de baja correctamente
    def test_p_1_action_action_dar_de_alta(self):
        print("PRIMER TEST")
        print("\n")
        #Solo el segundo esta dado de baja ([1]), por lo tanto, el primero ([0]) esta dado de alta.
        print("ANTES: Dada de alta: " + str(self.employee_without_image_2[1].dada_alta) + " - Fecha de baja: " + str(self.employee_without_image_2[1].fecha_de_baja))
        print("\n")
        self.employee_without_image_2[1].action_dar_de_alta()
        print("DESPUES: Dada de alta: " + str(self.employee_without_image_2[1].dada_alta) + " - Fecha de alta: " + str(self.employee_without_image_2[1].fecha_de_alta))
        print("\n")
        var = self.assertRecordValues(self.employee_without_image_2,[
            {'name': 'Prueba', 'dada_alta': True},
            {'name': 'Prueba2', 'dada_alta': True}
        ])

        return var

    #test para comprobar que no se puede dar de alta si ya esta dada de alta
    def test_p_2_action_action_dar_de_alta_falla(self):
        print("SEGUNDO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Dada de alta: " + str(self.employee_without_image_2[0].dada_alta) + " - Fecha de baja: " + str(self.employee_without_image_2[0].fecha_de_baja))
        print("\n")
        try:
            self.employee_without_image_2[0].action_dar_de_alta()
            print("DESPUES: Dada de alta: " + str(self.employee_without_image_2[0].dada_alta) + " - Fecha de alta: " + str(self.employee_without_image_2[0].fecha_de_alta))
            print("\n")
            var = self.assertRecordValues(self.employee_without_image_2,[
                {'name': 'Prueba', 'dada_alta': True},
                {'name': 'Prueba2', 'dada_alta': False}
            ])
            return var
        except:
            print("Ya estaba dada de alta por lo que salta la exception UserError")
            print("\n")
            var = self.assertRecordValues(self.employee_without_image_2,[
                {'name': 'Prueba', 'dada_alta': True},
                {'name': 'Prueba2', 'dada_alta': False}
            ])
            return var


    #test para comprobar que se da de baja si correctamente
    def test_p_3_action_action_dar_de_baja(self):
        print("TERCER TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Dada de alta: " + str(self.employee_without_image_2[0].dada_alta) + " - Fecha de baja: " + str(self.employee_without_image_2[0].fecha_de_baja))
        print("\n")

        self.employee_without_image_2[0].action_dar_de_baja()

        print("DESPUES: Dada de alta: " + str(self.employee_without_image_2[0].dada_alta) + " - Fecha de baja: " + str(self.employee_without_image_2[0].fecha_de_baja))
        print("\n")
        var = self.assertRecordValues(self.employee_without_image_2,[
                {'name': 'Prueba', 'dada_alta': False},
                {'name': 'Prueba2', 'dada_alta': False}
                ])
        return var


    #test para comprobar que no se puede dar de alta si ya esta dada de alta
    def test_p_4_action_action_dar_de_baja_falla(self):
        print("CUARTO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Dada de alta: " + str(self.employee_without_image_2[1].dada_alta) + " - Fecha de baja: " + str(self.employee_without_image_2[1].fecha_de_baja))
        print("\n")
        try:
            self.employee_without_image_2[1].action_dar_de_baja()
            print("DESPUES: Dada de alta: " + str(self.employee_without_image_2[1].dada_alta) + " - Fecha de baja: " + str(self.employee_without_image_2[1].fecha_de_baja))
            print("\n")
            var = self.assertRecordValues(self.employee_without_image_2,[
                {'name': 'Prueba', 'dada_alta': True},
                {'name': 'Prueba2', 'dada_alta': False}
            ])
            return var
        except:
            print("Ya estaba dada de baja por lo que salta la exception UserError")
            print("\n")
            var = self.assertRecordValues(self.employee_without_image_2,[
                {'name': 'Prueba', 'dada_alta': True},
                {'name': 'Prueba2', 'dada_alta': False}
            ])
            return var

    #test para comprobar que no se puede crear otro empleado con el mismo usuario de inicio de sesión
    def test_p_5_crear_usuario_con_mismo_inicio_sesion(self):
        print("QUINTO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Usuario: " + str(self.employee_without_image_2[0].user_id.name))
        print("\n")
        try:
            self.employee_without_image_falla = self.env['hr.employee'].create({
            'user_id': self.user_without_image_2[0].id,
            'image_1920': False,
        })
        except:
            print("Ya existe ese inicio de sesión, entonces falla.")
            print("\n")
            var = True
            return var

    #test para comprobar que no se puede crear una socia con el mismo usuario de inicio de sesión que un empleado
    def test_p_6_crear_usuario_con_mismo_inicio_sesion_que_empleado(self):
        print("SEXTO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Usuario empleado: " + str(self.employee_without_image_2[0].user_id.name))
        print("\n")
        try:
            fecha_normal = datetime.date.today() - relativedelta(years=23)

            self.socias = self.env['usuario.socia'].create([
                {
                    'tiene_dni': True, 
                    'dni': "66727211S",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_normal,
                    'peso_actual': 65.0,
                    'altura_actual': 1.75,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar confianza en mí misma.",
                    'user_id': self.employee_without_image_2[0].user_id.id
                }
            ])
        except:
            print("Ya existe ese inicio de sesión, entonces falla.")
            print("\n")
            var = True
            return var

    #test para comprobar que no se puede crear otro empleado con el mismo usuario de inicio de sesión que una socia
    def test_p_7_crear_usuario_con_mismo_inicio_sesion_que_socia(self):
        print("SEPTIMO TEST")
        print("\n")

        print("ANTES: Usuario socia: " + str(self.socias.user_id.login))
        print("\n")
        try:
            self.employee_without_image_2 = self.env['hr.employee'].create({
            'name': 'Prueba',
            'user_id': self.socias.user_id.id,
            'image_1920': False,
        })
        except:
            print("Ya existe ese inicio de sesión, entonces falla.")
            print("\n")
            var = True
            return var


    #test para comprobar que se pueden editar los datos de los empleados
    def test_p_8_editar_datos_empleado(self):
        print("OCTAVO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Nombre empleado: " + str(self.employee_without_image_2[0].name))
        print("\n")

        self.employee_without_image_2_2 = self.employee_without_image_2[0].write({
            'name': 'José María'
        })
        
        print("DESPUES: Nombre empleado: " + str(self.employee_without_image_2[0].name))
        print("\n")
        var = self.assertEqual(self.employee_without_image_2[0].name, 'José María')
        return var
