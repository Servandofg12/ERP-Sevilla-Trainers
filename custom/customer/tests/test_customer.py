from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
import datetime
from dateutil.relativedelta import relativedelta

@tagged('customer')
class CustomerTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(CustomerTestCase, cls).setUpClass()
        print("\n")
        print("REALIZANDO SETUP DE TESTS DEL MODULO SOCIA")
        print("\n")

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.

        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        fecha_normal = hoy - relativedelta(years=23)

        cls.socias = cls.env['customer.customer'].create([
            {
                'have_dni': True, 
                'dni': "66727272Z",
                'name': "Hola",
                'surnames': "Ejemplo Ejemplo",
                'birth_date': fecha_normal,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "transfer",
                'goal': "Quiero ganar masa muscular"
            },
            {
                'have_dni': True, 
                'dni': "66727272A",
                'name': "Hello",
                'surnames': "Example Example",
                'birth_date': fecha_estudiante,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "in_hand",
                'goal': "Quiero ganar masa muscular",
                'registered': False,
                'unsubscribe_date': hoy - relativedelta(months=2)
            }
        ])

        cls.maquinas =cls.env['training.machine'].create([
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

        cls.socias = cls.env['customer.customer'].create(
                {
                    'have_dni': True, 
                    'dni': "66727211S",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_normal,
                    'actual_weight': 65.0,
                    'actual_height': 1.75,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar confianza en mí misma.",
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

        self.socias = self.env['customer.customer'].create([
            {
                'have_dni': True, 
                'dni': "72727272Z",
                'name': "Hola",
                'surnames': "Ejemplo Ejemplo",
                'birth_date': fecha_normal,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "transfer",
                'goal': "Quiero ganar masa muscular"
            },
            {
                'have_dni': True, 
                'dni': "72727272A",
                'name': "Hello",
                'surnames': "Example Example",
                'birth_date': fecha_estudiante,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "in_hand",
                'goal': "Quiero ganar masa muscular"
            }
        ])

        print("¿Dada de alta? " + str(self.socias[0].registered))
        print("Nombre completo: " + str(self.socias[0].name) + " " + str(self.socias[0].surnames))
        print("Edad: " + str(self.socias[0].age))
        print("Tipo de pase: " + str(self.socias[0].season_pass))
        print("Coste del pase: " + str(self.socias[0].season_pass_cost))
        print("\n")

        print("¿Dada de alta? " + str(self.socias[1].registered))
        print("Nombre completo: " + str(self.socias[1].name) + " " + str(self.socias[0].surnames))
        print("Edad: " + str(self.socias[1].age))
        print("Tipo de pase: " + str(self.socias[1].season_pass))
        print("Coste del pase: " + str(self.socias[1].season_pass_cost))
        print("\n")

        var = self.assertEqual(self.socias[0].registered, True)
        var2 = self.assertEqual(self.socias[1].registered, True)
        result = var and var2
        return result


    #test donde el name de la clienta no es correcto
    def test_p_02_socia_nombre_con_mayusculas(self):
        print("\n")
        print("SEGUNDO TEST")
        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        self.socias = self.env['customer.customer']
        try:
            self.socias.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "HoLa",#falla aqui
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_estudiante,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar masa muscular"
                }])
        except:
            print("El name contiene mayusculas y falla al crear la socia")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    #test donde el name de la clienta no es correcto
    def test_p_03_socia_nombre_con_numero(self):
        print("\n")
        print("TERCER TEST")
        hoy = datetime.date.today()
        fecha_estudiante = hoy - relativedelta(years=19)
        self.socias = self.env['customer.customer']
        try:
            self.socias.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "H9La",#falla aqui
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_estudiante,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar masa muscular"
                }])
        except:
            print("El name contiene un numero y falla al crear la socia")
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
        self.socias = self.env['customer.customer']
        try:
            self.socias.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "EjemPlo EjemPlo",#falla aqui
                    'birth_date': fecha_estudiante,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar masa muscular"
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
        self.socias = self.env['customer.customer']
        try:
            self.socias.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo 2Ejemplo",#falla aqui
                    'birth_date': fecha_estudiante,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar masa muscular"
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
        self.socias = self.env['customer.customer']
        try:
            var = self.assertEqual(False, True)
            self.socias.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,#falla aqui
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar masa muscular"
                }])
            return var
        except:
            print("La age es menor a 14 años y falla al crear la socia")
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
        self.socias = self.env['customer.customer']
        try:
            self.socias.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,
                    'actual_weight': -200.0,#falla aqui
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar masa muscular"
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
        self.socias = self.env['customer.customer']
        try:
            self.socias.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,
                    'actual_weight': 70.0,
                    'actual_height': -1.80,#falla aqui
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar masa muscular"
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
        self.socias = self.env['customer.customer']
        try:
            self.socias.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,#falla aqui
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar masa muscular"
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
            self.socias = self.env['customer.customer'].create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_normal,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar masa muscular"
                },
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Example Example",
                    'birth_date': fecha_estudiante,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "in_hand",
                    'goal': "Quiero ganar masa muscular"
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
            self.socias = self.env['customer.customer'].create([
                {
                    'have_dni': False, 
                    'nie': "72727272Z",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_normal,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "Quiero ganar masa muscular"
                },
                {
                    'have_dni': False, 
                    'nie': "72727272Z",
                    'name': "Hello",
                    'surnames': "Example Example",
                    'birth_date': fecha_estudiante,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "in_hand",
                    'goal': "Quiero ganar masa muscular"
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
        print("ANTES: Dada de alta: " + str(self.socias[1].registered) + " - Fecha de baja: " + str(self.socias[1].unsubscribe_date))
        print("\n")
        self.socias[1].action_register()
        print("DESPUES: Dada de alta: " + str(self.socias[1].registered) + " - Fecha de alta: " + str(self.socias[1].register_date))
        print("\n")
        var = self.assertRecordValues(self.socias,[
            {'name': 'Hola', 'registered': True},
            {'name': 'Hello', 'registered': True}
        ])

        return var

    #test para comprobar que no se puede dar de alta si ya esta dada de alta
    def test_p_13_action_action_dar_de_alta_falla(self):
        print("DECIMO TERCER TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Dada de alta: " + str(self.socias[0].registered) + " - Fecha de baja: " + str(self.socias[0].unsubscribe_date))
        print("\n")
        try:
            self.socias[0].action_register()
            print("DESPUES: Dada de alta: " + str(self.socias[0].registered) + " - Fecha de alta: " + str(self.socias[0].register_date))
            print("\n")
            var = self.assertRecordValues(self.socias,[
                {'name': 'Hola', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var
        except:
            print("Ya estaba dada de alta por lo que salta la exception UserError")
            print("\n")
            var = self.assertRecordValues(self.socias,[
                {'name': 'Hola', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var


    #test para comprobar que se da de baja si correctamente
    def test_p_14_action_action_dar_de_baja(self):
        print("DECIMO CUARTO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Dada de alta: " + str(self.socias[0].registered) + " - Fecha de baja: " + str(self.socias[0].unsubscribe_date))
        print("\n")

        self.socias[0].action_unsubscribe()

        print("DESPUES: Dada de alta: " + str(self.socias[0].registered) + " - Fecha de baja: " + str(self.socias[0].unsubscribe_date))
        print("\n")
        var = self.assertRecordValues(self.socias,[
                {'name': 'Hola', 'registered': False},
                {'name': 'Hello', 'registered': False}
                ])
        return var


    #test para comprobar que no se puede dar de alta si ya esta dada de alta
    def test_p_15_action_action_dar_de_baja_falla(self):
        print("DECIMO QUINTO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Dada de alta: " + str(self.socias[1].registered) + " - Fecha de baja: " + str(self.socias[1].unsubscribe_date))
        print("\n")
        try:
            self.socias[1].action_unsubscribe()
            print("DESPUES: Dada de alta: " + str(self.socias[1].registered) + " - Fecha de baja: " + str(self.socias[1].unsubscribe_date))
            print("\n")
            var = self.assertRecordValues(self.socias,[
                {'name': 'Hola', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var
        except:
            print("Ya estaba dada de baja por lo que salta la exception UserError")
            print("\n")
            var = self.assertRecordValues(self.socias,[
                {'name': 'Hola', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var


    #TESTS PARA COMPROBAR LA FUNCIONALIDAD DE REVISION MENSUAL -----------------------------------------------------------------------

    #test para comprobar que funciona correctamente la revision mensual
    def test_p_16_revision_mensual_correcta(self):
        print("DECIMO SEXTO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Número de revisiones: " + str(len(self.socias[0].monthly_review_ids)))
        print("Peso de la socia: " + str(self.socias[0].actual_weight))
        print("Altura de la socia: " + str(self.socias[0].actual_height))
        print("\n")
        self.revision = self.env['monthly.review']
        self.revision.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today(),
                    'customer_id': self.socias[0].id
                }])

        print("DESPUES: Número de revisiones: " + str(len(self.socias[0].monthly_review_ids)))
        print("Peso de la socia: " + str(self.socias[0].actual_weight))
        print("Altura de la socia: " + str(self.socias[0].actual_height))
        print("\n")

        var = self.assertEqual(1, len(self.socias[0].monthly_review_ids))
        return var

    #test para comprobar que no se pueden crear 2 en el mismo mes
    def test_p_17_revision_mensual_falla(self):
        print("DECIMO SEPTIMO TEST")
        print("\n")

        self.revision = self.env['monthly.review']
        self.revision.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today(),
                    'customer_id': self.socias[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Número de revisiones: " + str(len(self.socias[0].monthly_review_ids)))
        print("\n")

        try:
            print("Intentando añadir otra revisión con la misma fecha...")
            self.revision_falla = self.env['monthly.review']
            self.revision_falla.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today(),
                    'customer_id': self.socias[0].id
                }])
        except:
            print("Falla porque se debe esperar un mes para poder hacer otra revisión.")
            print("DESPUES: Número de revisiones: " + str(len(self.socias[0].monthly_review_ids)))
            print("\n")

            var = self.assertEqual(1, len(self.socias[0].monthly_review_ids))
            return var
        
    #test para comprobar que no se pueden crear 2 en el mismo mes
    def test_p_18_revision_mensual_falla(self):
        print("DECIMO OCTAVO TEST")
        print("\n")

        self.revision = self.env['monthly.review']
        self.revision.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today(),
                    'customer_id': self.socias[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES: Número de revisiones: " + str(len(self.socias[0].monthly_review_ids)))
        print("\n")

        try:
            print("Intentando añadir otra revisión con la misma fecha...")
            self.revision_falla = self.env['monthly.review']
            self.revision_falla.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today() + relativedelta(months=1) - relativedelta(days=1),
                    'customer_id': self.socias[0].id
                }])
        except:
            print("Falla porque se debe esperar un mes para poder hacer otra revisión.")
            print("DESPUES: Número de revisiones: " + str(len(self.socias[0].monthly_review_ids)))
            print("\n")

            var = self.assertEqual(1, len(self.socias[0].monthly_review_ids))
            return var

    #test para comprobar que se pueden crear 2 en distinto mes
    def test_p_19_dos_revisiones_mensuales_correctas(self):
        print("DECIMO NOVENO TEST")
        print("\n")

        print("ANTES: Número de revisiones: " + str(len(self.socias[0].monthly_review_ids)))
        print("\n")

        self.revision = self.env['monthly.review']
        self.revision.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today() - relativedelta(months=1),
                    'customer_id': self.socias[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("DESPUES de una revision: Número de revisiones: " + str(len(self.socias[0].monthly_review_ids)))
        print("\n")
        
        self.revision_falla = self.env['monthly.review']
        self.revision_falla.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today(),
                    'customer_id': self.socias[0].id
                }])

        print("DESPUES: Número de revisiones: " + str(len(self.socias[0].monthly_review_ids)))
        print("\n")

        var = self.assertEqual(2, len(self.socias[0].monthly_review_ids))
        return var

    
    #TESTS PARA COMPROBAR LA FUNCIONALIDAD DE ENTRENAMIENTO PERSONAL -----------------------------------------------------------------------

    #test para comprobar que se pueden crear un entrenamiento
    def test_p_20_entrenamiento_personal(self):
        print("VIGESIMO TEST")
        print("\n")

        print("ANTES: Número de entrenamientos: " + str(len(self.socias[0].customer_training_ids)))
        print("\n")

        self.entrenamiento = self.env['customer.training']
        self.entrenamiento.create([
                {
                    'name': "Mi entrenamiento",
                    'numb_turns': 1,
                    'machine_use': True,
                    'training_machine_ids': self.maquinas[0],
                    'customer_id': self.socias[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("DESPUES: Número de entrenamientos: " + str(len(self.socias[0].customer_training_ids)))
        print("\n")

        var = self.assertEqual(1, len(self.socias[0].customer_training_ids))
        return var

    #test para comprobar que se pueden crear 2 entrenamientos
    def test_p_21_dos_entrenamientos_personales(self):
        print("VIGESIMO PRIMER TEST")
        print("\n")

        print("ANTES: Número de entrenamientos: " + str(len(self.socias[0].customer_training_ids)))
        print("\n")

        self.entrenamiento = self.env['customer.training']
        self.entrenamiento.create([
                {
                    'name': "Mi entrenamiento",
                    'numb_turns': 1,
                    'machine_use': True,
                    'training_machine_ids': self.maquinas[0],
                    'customer_id': self.socias[0].id
                },
                {
                    'name': "Mi entrenamiento 2",
                    'numb_turns': 2,
                    'machine_use': True,
                    'training_machine_ids': [self.maquinas[0].id, self.maquinas[1].id],
                    'customer_id': self.socias[0].id
                }
                ])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("DESPUES: Número de entrenamientos: " + str(len(self.socias[0].customer_training_ids)))
        print("\n")

        var = self.assertEqual(2, len(self.socias[0].customer_training_ids))
        return var
    
    #TEST DE EDICION DE DATOS ---------------------------------------------------------------------------------------------------------------

    #test para comprobar que se pueden editar los datos de las socias
    def test_p_22_editar_datos_socia(self):
        print("VIGESIMO SEGUNDO TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("ANTES:")
        print("Nombre: " + str(self.socias[0].name))
        print("Apellidos: " + str(self.socias[0].surnames))
        print("Fecha nacimiento: " + str(self.socias[0].birth_date))
        print("Edad: " + str(self.socias[0].age))
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
        print("Edad: " + str(self.socias[0].age))
        print("\n")
        var1 = self.assertEqual(self.socias[0].name, 'José María')
        var2 = self.assertEqual(self.socias[0].surnames, 'Iglesias Bellido')
        var3 = self.assertEqual(self.socias[0].birth_date, datetime.date.today() - relativedelta(years=58))
        var4 = self.assertEqual(self.socias[0].age, 58)
        res = var1 and (var2 and (var3 and (var4)))
        return res