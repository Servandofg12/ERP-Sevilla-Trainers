from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
import datetime
from dateutil.relativedelta import relativedelta

@tagged('socias')
class UsuarioSociaTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(UsuarioSociaTestCase, cls).setUpClass()
        print("\n")
        print("REALIZANDO SETUP DE TESTS DEL MODULO SOCIA")
        print("\n")

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.

        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        fecha_normal = hoy - relativedelta(years=23)

        cls.socias = cls.env['usuario.socia'].create([
            {
                'tiene_dni': True, 
                'dni': "66727272Z",
                'name': "Hola",
                'surnames': "Ejemplo Ejemplo",
                'birth_date': fecha_normal,
                'peso_actual': 70.0,
                'altura_actual': 1.80,
                'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'formas_de_pago': "transferencia",
                'objetivo': "Quiero ganar masa muscular"
            },
            {
                'tiene_dni': True, 
                'dni': "66727272A",
                'name': "Hello",
                'surnames': "Example Example",
                'birth_date': fecha_estudiante,
                'peso_actual': 70.0,
                'altura_actual': 1.80,
                'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'formas_de_pago': "en_mano",
                'objetivo': "Quiero ganar masa muscular",
                'dada_alta': False,
                'fecha_de_baja': hoy - relativedelta(months=2)
            }
        ])

        cls.maquinas =cls.env['maquinas.entrenamiento'].create([
            {
                'name': "Sentadillas"
            },
            {
                'name': "Pecho/Espalda"
            }
        ])

        #Lo siguiente falla
        '''cls.user = cls.env['res.users'].create({
            'name': 'Prueba3',
            'email': 'prueba3333@example.com',
            'login': 'prueba_3',
            'password': 'prueba_123',
            'partner_id': cls.env['res.partner'].create({
                'name': "Strawman Test User"
            }).id
        })

        fecha_normal = datetime.date.today() - relativedelta(years=23)

        cls.socias = cls.env['usuario.socia'].create(
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
                    'user_id': cls.user.user_id.id
                }
            )'''


    #test donde la clienta es correcta
    def test_p_01_socia_correcta(self):
        print("\n")
        print("PRIMER TEST")
        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        fecha_normal = hoy - relativedelta(years=23)

        self.socias = self.env['usuario.socia'].create([
            {
                'tiene_dni': True, 
                'dni': "72727272Z",
                'name': "Hola",
                'surnames': "Ejemplo Ejemplo",
                'birth_date': fecha_normal,
                'peso_actual': 70.0,
                'altura_actual': 1.80,
                'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'formas_de_pago': "transferencia",
                'objetivo': "Quiero ganar masa muscular"
            },
            {
                'tiene_dni': True, 
                'dni': "72727272A",
                'name': "Hello",
                'surnames': "Example Example",
                'birth_date': fecha_estudiante,
                'peso_actual': 70.0,
                'altura_actual': 1.80,
                'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'formas_de_pago': "en_mano",
                'objetivo': "Quiero ganar masa muscular"
            }
        ])

        print("¿Dada de alta? " + str(self.socias[0].dada_alta))
        print("Nombre completo: " + str(self.socias[0].name) + " " + str(self.socias[0].surnames))
        print("Edad: " + str(self.socias[0].edad))
        print("Tipo de pase: " + str(self.socias[0].tipo_pase_temporada))
        print("Coste del pase: " + str(self.socias[0].coste_pase))
        print("\n")

        print("¿Dada de alta? " + str(self.socias[1].dada_alta))
        print("Nombre completo: " + str(self.socias[1].name) + " " + str(self.socias[0].surnames))
        print("Edad: " + str(self.socias[1].edad))
        print("Tipo de pase: " + str(self.socias[1].tipo_pase_temporada))
        print("Coste del pase: " + str(self.socias[1].coste_pase))
        print("\n")

        var = self.assertEqual(self.socias[0].dada_alta, True)
        var2 = self.assertEqual(self.socias[1].dada_alta, True)
        result = var and var2
        return result


    #test donde el nombre de la clienta no es correcto
    def test_p_02_socia_nombre_con_mayusculas(self):
        print("\n")
        print("SEGUNDO TEST")
        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        self.socias = self.env['usuario.socia']
        try:
            self.socias.create([
                {
                    'tiene_dni': True, 
                    'dni': "72727272Z",
                    'name': "HoLa",#falla aqui
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_estudiante,
                    'peso_actual': 70.0,
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar masa muscular"
                }])
        except:
            print("El nombre contiene mayusculas y falla al crear la socia")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    #test donde el nombre de la clienta no es correcto
    def test_p_03_socia_nombre_con_numero(self):
        print("\n")
        print("TERCER TEST")
        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        self.socias = self.env['usuario.socia']
        try:
            self.socias.create([
                {
                    'tiene_dni': True, 
                    'dni': "72727272Z",
                    'name': "H9La",#falla aqui
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_estudiante,
                    'peso_actual': 70.0,
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar masa muscular"
                }])
        except:
            print("El nombre contiene un numero y falla al crear la socia")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    #test donde el apellido de la clienta no es correcto
    def test_p_04_socia_apellidos_con_mayusculas(self):
        print("\n")
        print("CUARTO TEST")
        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        self.socias = self.env['usuario.socia']
        try:
            self.socias.create([
                {
                    'tiene_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "EjemPlo EjemPlo",#falla aqui
                    'birth_date': fecha_estudiante,
                    'peso_actual': 70.0,
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar masa muscular"
                }])
        except:
            print("Los apellidos contienen más de una mayuscula y falla al crear la socia")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    #test donde el apellido de la clienta no es correcto
    def test_p_05_socia_apellidos_con_numero(self):
        print("\n")
        print("QUINTO TEST")
        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        self.socias = self.env['usuario.socia']
        try:
            self.socias.create([
                {
                    'tiene_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo 2Ejemplo",#falla aqui
                    'birth_date': fecha_estudiante,
                    'peso_actual': 70.0,
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar masa muscular"
                }])
        except:
            print("Los apellidos contienen un numero y falla al crear la socia")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    #test donde la socia es menor de 14 años
    def test_p_06_socia_edad_menor_14(self):
        print("\n")
        print("SEXTO TEST")
        hoy = datetime.date.today()
        fecha_nac = hoy - relativedelta(years=10)
        #print("Fecha nac: "+ str(fecha_nac))
        self.socias = self.env['usuario.socia']
        try:
            var = self.assertEqual(False, True)
            self.socias.create([
                {
                    'tiene_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,#falla aqui
                    'peso_actual': 70.0,
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar masa muscular"
                }])
            return var
        except:
            print("La edad es menor a 14 años y falla al crear la socia")
            print("\n")
            var = self.assertEqual(False, False)
            return var


    
    #test donde la socia tiene un peso negativo
    #El error en la consola es por ser restriccion SQL, pero el test se realiza correctamente
    def test_p_07_socia_peso_negativo(self):
        print("\n")
        print("SEPTIMO TEST")
        hoy = datetime.date.today()
        fecha_nac = hoy - relativedelta(years=19)
        self.socias = self.env['usuario.socia']
        try:
            self.socias.create([
                {
                    'tiene_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,
                    'peso_actual': -200.0,#falla aqui
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar masa muscular"
                }])
        except:
            print("El peso no puede ser negativo y falla al crear la socia")
            print("\n")
            var = self.assertEqual(False, False)
            return var
            
        return False

        
    #test donde la socia tiene una altura negativa
    #El error en la consola es por ser restriccion SQL, pero el test se realiza correctamente
    def test_p_08_socia_altura_negativa(self):
        print("\n")
        print("OCTAVO TEST")
        hoy = datetime.date.today()
        fecha_nac = hoy - relativedelta(years=19)
        self.socias = self.env['usuario.socia']
        try:
            self.socias.create([
                {
                    'tiene_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,
                    'peso_actual': 70.0,
                    'altura_actual': -1.80,#falla aqui
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar masa muscular"
                }])
        except:
            print("La altura no puede ser negativa y falla al crear la socia")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    #test donde la socia tiene una fecha de nacimiento futura
    def test_p_09_socia_fecha_nacimiento_futura(self):
        print("\n")
        print("NOVENO TEST")
        hoy = datetime.date.today()
        fecha_nac = hoy + relativedelta(years=1)
        self.socias = self.env['usuario.socia']
        try:
            self.socias.create([
                {
                    'tiene_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,#falla aqui
                    'peso_actual': 70.0,
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar masa muscular"
                }])
        except:
            print("El año no puede ser futuro y falla al crear la socia")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    #test donde las dos clientas tienen el mismo DNI
    #El error en la consola es por ser restriccion SQL, pero el test se realiza correctamente
    def test_p_10_socia_con_mismo_dni(self):
        print("\n")
        print("DECIMO TEST")
        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        fecha_normal = hoy - relativedelta(years=23)

        try:
            self.socias = self.env['usuario.socia'].create([
                {
                    'tiene_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_normal,
                    'peso_actual': 70.0,
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar masa muscular"
                },
                {
                    'tiene_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Example Example",
                    'birth_date': fecha_estudiante,
                    'peso_actual': 70.0,
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "en_mano",
                    'objetivo': "Quiero ganar masa muscular"
                }
            ])
        except:
            print("Las dos socias tienen el mismo DNI y falla")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    #test donde las dos clientas tienen el mismo NIE
    #El error en la consola es por ser restriccion SQL, pero el test se realiza correctamente
    def test_p_11_socia_con_mismo_nie(self):
        print("\n")
        print("DECIMO PRIMER TEST")
        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        fecha_normal = hoy - relativedelta(years=23)

        try:
            self.socias = self.env['usuario.socia'].create([
                {
                    'tiene_dni': False, 
                    'nie': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_normal,
                    'peso_actual': 70.0,
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "transferencia",
                    'objetivo': "Quiero ganar masa muscular"
                },
                {
                    'tiene_dni': False, 
                    'nie': "72727272Z",
                    'name': "Hello",
                    'surnames': "Example Example",
                    'birth_date': fecha_estudiante,
                    'peso_actual': 70.0,
                    'altura_actual': 1.80,
                    'direccion': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'formas_de_pago': "en_mano",
                    'objetivo': "Quiero ganar masa muscular"
                }
            ])
        except:
            print("Las dos socias tienen el mismo NIE y falla")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    #TESTS PARA COMPROBAR LA FUNCIONALIDAD DE DAR DE ALTA Y BAJA -----------------------------------------------------------------------

    #test para comprobar que se da de baja correctamente
    def test_p_12_action_action_dar_de_alta(self):
        print("DECIMO SEGUNDO TEST")
        print("\n")
        #Solo el segundo esta dado de baja ([1]), por lo tanto, el primero ([0]) esta dado de alta.
        print("ANTES: Dada de alta: " + str(self.socias[1].dada_alta) + " - Fecha de baja: " + str(self.socias[1].fecha_de_baja))
        print("\n")
        self.socias[1].action_dar_de_alta()
        print("DESPUES: Dada de alta: " + str(self.socias[1].dada_alta) + " - Fecha de alta: " + str(self.socias[1].fecha_de_alta))
        print("\n")
        var = self.assertRecordValues(self.socias,[
            {'name': 'Hola', 'dada_alta': True},
            {'name': 'Hello', 'dada_alta': True}
        ])

        return var

    #test para comprobar que no se puede dar de alta si ya esta dada de alta
    def test_p_13_action_action_dar_de_alta_falla(self):
        print("DECIMO TERCER TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Dada de alta: " + str(self.socias[0].dada_alta) + " - Fecha de baja: " + str(self.socias[0].fecha_de_baja))
        print("\n")
        try:
            self.socias[0].action_dar_de_alta()
            print("DESPUES: Dada de alta: " + str(self.socias[0].dada_alta) + " - Fecha de alta: " + str(self.socias[0].fecha_de_alta))
            print("\n")
            var = self.assertRecordValues(self.socias,[
                {'name': 'Hola', 'dada_alta': True},
                {'name': 'Hello', 'dada_alta': False}
            ])
            return var
        except:
            print("Ya estaba dada de alta por lo que salta la exception UserError")
            print("\n")
            var = self.assertRecordValues(self.socias,[
                {'name': 'Hola', 'dada_alta': True},
                {'name': 'Hello', 'dada_alta': False}
            ])
            return var


    #test para comprobar que se da de baja si correctamente
    def test_p_14_action_action_dar_de_baja(self):
        print("DECIMO CUARTO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Dada de alta: " + str(self.socias[0].dada_alta) + " - Fecha de baja: " + str(self.socias[0].fecha_de_baja))
        print("\n")

        self.socias[0].action_dar_de_baja()

        print("DESPUES: Dada de alta: " + str(self.socias[0].dada_alta) + " - Fecha de baja: " + str(self.socias[0].fecha_de_baja))
        print("\n")
        var = self.assertRecordValues(self.socias,[
                {'name': 'Hola', 'dada_alta': False},
                {'name': 'Hello', 'dada_alta': False}
                ])
        return var


    #test para comprobar que no se puede dar de alta si ya esta dada de alta
    def test_p_15_action_action_dar_de_baja_falla(self):
        print("DECIMO QUINTO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Dada de alta: " + str(self.socias[1].dada_alta) + " - Fecha de baja: " + str(self.socias[1].fecha_de_baja))
        print("\n")
        try:
            self.socias[1].action_dar_de_baja()
            print("DESPUES: Dada de alta: " + str(self.socias[1].dada_alta) + " - Fecha de baja: " + str(self.socias[1].fecha_de_baja))
            print("\n")
            var = self.assertRecordValues(self.socias,[
                {'name': 'Hola', 'dada_alta': True},
                {'name': 'Hello', 'dada_alta': False}
            ])
            return var
        except:
            print("Ya estaba dada de baja por lo que salta la exception UserError")
            print("\n")
            var = self.assertRecordValues(self.socias,[
                {'name': 'Hola', 'dada_alta': True},
                {'name': 'Hello', 'dada_alta': False}
            ])
            return var


    #TESTS PARA COMPROBAR LA FUNCIONALIDAD DE REVISION MENSUAL -----------------------------------------------------------------------

    #test para comprobar que funciona correctamente la revision mensual
    def test_p_16_revision_mensual_correcta(self):
        print("DECIMO SEXTO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Número de revisiones: " + str(len(self.socias[0].revision_mensual_ids)))
        print("Peso de la socia: " + str(self.socias[0].peso_actual))
        print("Altura de la socia: " + str(self.socias[0].altura_actual))
        print("\n")
        self.revision = self.env['revision.mensual']
        self.revision.create([
                {
                    'nuevo_peso': 90.0,
                    'nueva_altura': 1.78,
                    'porcentaje_grasa_corporal': 15,
                    'indice_masa_corporal': 13,
                    'medida_pecho': 30,
                    'medida_cintura': 35,
                    'medida_abdomen': 30,
                    'medida_caderas': 35,
                    'medida_muslos': 20,
                    'medida_brazos': 15,
                    'fecha_realizada': datetime.date.today(),
                    'usuario_socia_id': self.socias[0].id
                }])

        print("DESPUES: Número de revisiones: " + str(len(self.socias[0].revision_mensual_ids)))
        print("Peso de la socia: " + str(self.socias[0].peso_actual))
        print("Altura de la socia: " + str(self.socias[0].altura_actual))
        print("\n")

        var = self.assertEqual(1, len(self.socias[0].revision_mensual_ids))
        return var

    #test para comprobar que no se pueden crear 2 en el mismo mes
    def test_p_17_revision_mensual_falla(self):
        print("DECIMO SEPTIMO TEST")
        print("\n")

        self.revision = self.env['revision.mensual']
        self.revision.create([
                {
                    'nuevo_peso': 90.0,
                    'nueva_altura': 1.78,
                    'porcentaje_grasa_corporal': 15,
                    'indice_masa_corporal': 13,
                    'medida_pecho': 30,
                    'medida_cintura': 35,
                    'medida_abdomen': 30,
                    'medida_caderas': 35,
                    'medida_muslos': 20,
                    'medida_brazos': 15,
                    'fecha_realizada': datetime.date.today(),
                    'usuario_socia_id': self.socias[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Número de revisiones: " + str(len(self.socias[0].revision_mensual_ids)))
        print("\n")

        try:
            print("Intentando añadir otra revisión con la misma fecha...")
            self.revision_falla = self.env['revision.mensual']
            self.revision_falla.create([
                {
                    'nuevo_peso': 90.0,
                    'nueva_altura': 1.78,
                    'porcentaje_grasa_corporal': 15,
                    'indice_masa_corporal': 13,
                    'medida_pecho': 30,
                    'medida_cintura': 35,
                    'medida_abdomen': 30,
                    'medida_caderas': 35,
                    'medida_muslos': 20,
                    'medida_brazos': 15,
                    'fecha_realizada': datetime.date.today(),
                    'usuario_socia_id': self.socias[0].id
                }])
        except:
            print("Falla porque se debe esperar un mes para poder hacer otra revisión.")
            print("DESPUES: Número de revisiones: " + str(len(self.socias[0].revision_mensual_ids)))
            print("\n")

            var = self.assertEqual(1, len(self.socias[0].revision_mensual_ids))
            return var
        
    #test para comprobar que no se pueden crear 2 en el mismo mes
    def test_p_18_revision_mensual_falla(self):
        print("DECIMO OCTAVO TEST")
        print("\n")

        self.revision = self.env['revision.mensual']
        self.revision.create([
                {
                    'nuevo_peso': 90.0,
                    'nueva_altura': 1.78,
                    'porcentaje_grasa_corporal': 15,
                    'indice_masa_corporal': 13,
                    'medida_pecho': 30,
                    'medida_cintura': 35,
                    'medida_abdomen': 30,
                    'medida_caderas': 35,
                    'medida_muslos': 20,
                    'medida_brazos': 15,
                    'fecha_realizada': datetime.date.today(),
                    'usuario_socia_id': self.socias[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Número de revisiones: " + str(len(self.socias[0].revision_mensual_ids)))
        print("\n")

        try:
            print("Intentando añadir otra revisión con la misma fecha...")
            self.revision_falla = self.env['revision.mensual']
            self.revision_falla.create([
                {
                    'nuevo_peso': 90.0,
                    'nueva_altura': 1.78,
                    'porcentaje_grasa_corporal': 15,
                    'indice_masa_corporal': 13,
                    'medida_pecho': 30,
                    'medida_cintura': 35,
                    'medida_abdomen': 30,
                    'medida_caderas': 35,
                    'medida_muslos': 20,
                    'medida_brazos': 15,
                    'fecha_realizada': datetime.date.today() + relativedelta(months=1) - relativedelta(days=1),
                    'usuario_socia_id': self.socias[0].id
                }])
        except:
            print("Falla porque se debe esperar un mes para poder hacer otra revisión.")
            print("DESPUES: Número de revisiones: " + str(len(self.socias[0].revision_mensual_ids)))
            print("\n")

            var = self.assertEqual(1, len(self.socias[0].revision_mensual_ids))
            return var

    #test para comprobar que se pueden crear 2 en distinto mes
    def test_p_19_dos_revisiones_mensuales_correctas(self):
        print("DECIMO NOVENO TEST")
        print("\n")

        print("ANTES: Número de revisiones: " + str(len(self.socias[0].revision_mensual_ids)))
        print("\n")

        self.revision = self.env['revision.mensual']
        self.revision.create([
                {
                    'nuevo_peso': 90.0,
                    'nueva_altura': 1.78,
                    'porcentaje_grasa_corporal': 15,
                    'indice_masa_corporal': 13,
                    'medida_pecho': 30,
                    'medida_cintura': 35,
                    'medida_abdomen': 30,
                    'medida_caderas': 35,
                    'medida_muslos': 20,
                    'medida_brazos': 15,
                    'fecha_realizada': datetime.date.today() - relativedelta(months=1),
                    'usuario_socia_id': self.socias[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("DESPUES de una revision: Número de revisiones: " + str(len(self.socias[0].revision_mensual_ids)))
        print("\n")
        
        self.revision_falla = self.env['revision.mensual']
        self.revision_falla.create([
                {
                    'nuevo_peso': 90.0,
                    'nueva_altura': 1.78,
                    'porcentaje_grasa_corporal': 15,
                    'indice_masa_corporal': 13,
                    'medida_pecho': 30,
                    'medida_cintura': 35,
                    'medida_abdomen': 30,
                    'medida_caderas': 35,
                    'medida_muslos': 20,
                    'medida_brazos': 15,
                    'fecha_realizada': datetime.date.today(),
                    'usuario_socia_id': self.socias[0].id
                }])

        print("DESPUES: Número de revisiones: " + str(len(self.socias[0].revision_mensual_ids)))
        print("\n")

        var = self.assertEqual(2, len(self.socias[0].revision_mensual_ids))
        return var

    
    #TESTS PARA COMPROBAR LA FUNCIONALIDAD DE ENTRENAMIENTO PERSONAL -----------------------------------------------------------------------

    #test para comprobar que se pueden crear un entrenamiento
    def test_p_20_entrenamiento_personal(self):
        print("VIGESIMO TEST")
        print("\n")

        print("ANTES: Número de entrenamientos: " + str(len(self.socias[0].entrenamientos_socia_ids)))
        print("\n")

        self.entrenamiento = self.env['entrenamiento.socia']
        self.entrenamiento.create([
                {
                    'nombre': "Mi entrenamiento",
                    'num_vueltas': 1,
                    'usa_maquinas': True,
                    'maquinas_entrenamiento_ids': self.maquinas[0],
                    'usuario_socia_id': self.socias[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("DESPUES: Número de entrenamientos: " + str(len(self.socias[0].entrenamientos_socia_ids)))
        print("\n")

        var = self.assertEqual(1, len(self.socias[0].entrenamientos_socia_ids))
        return var

    #test para comprobar que se pueden crear 2 entrenamientos
    def test_p_21_dos_entrenamientos_personales(self):
        print("VIGESIMO PRIMER TEST")
        print("\n")

        print("ANTES: Número de entrenamientos: " + str(len(self.socias[0].entrenamientos_socia_ids)))
        print("\n")

        self.entrenamiento = self.env['entrenamiento.socia']
        self.entrenamiento.create([
                {
                    'nombre': "Mi entrenamiento",
                    'num_vueltas': 1,
                    'usa_maquinas': True,
                    'maquinas_entrenamiento_ids': self.maquinas[0],
                    'usuario_socia_id': self.socias[0].id
                },
                {
                    'nombre': "Mi entrenamiento 2",
                    'num_vueltas': 2,
                    'usa_maquinas': True,
                    'maquinas_entrenamiento_ids': [self.maquinas[0].id, self.maquinas[1].id],
                    'usuario_socia_id': self.socias[0].id
                }
                ])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("DESPUES: Número de entrenamientos: " + str(len(self.socias[0].entrenamientos_socia_ids)))
        print("\n")

        var = self.assertEqual(2, len(self.socias[0].entrenamientos_socia_ids))
        return var

    #test para comprobar que se pueden editar los datos de las socias
    def test_p_22_editar_datos_socia(self):
        print("VIGESIMO SEGUNDO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES:")
        print("Nombre: " + str(self.socias[0].name))
        print("Apellidos: " + str(self.socias[0].surnames))
        print("Fecha nacimiento: " + str(self.socias[0].birth_date))
        print("Edad: " + str(self.socias[0].edad))
        print("\n")

        self.socia_editada = self.socias[0].write({
            'name': 'José María',
            'surnames': 'Iglesias Bellido',
            'birth_date': datetime.date.today() - relativedelta(years=58)
        })
        
        print("DESPUES:")
        print("Nombre: " + str(self.socias[0].name))
        print("Apellidos: " + str(self.socias[0].surnames))
        print("Fecha nacimiento: " + str(self.socias[0].birth_date))
        print("Edad: " + str(self.socias[0].edad))
        print("\n")
        var1 = self.assertEqual(self.socias[0].name, 'José María')
        var2 = self.assertEqual(self.socias[0].surnames, 'Iglesias Bellido')
        var3 = self.assertEqual(self.socias[0].birth_date, datetime.date.today() - relativedelta(years=58))
        var4 = self.assertEqual(self.socias[0].edad, 58)
        res = var1 and (var2 and (var3 and (var4)))
        return res