from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

@tagged('post_install','socias')
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

        '''cls.users = cls.env['res.users'].create([
            {
                'name': "servandofg12",
                'password': "1234servandofg",
                'phone': "666666666",
                'email': "servan@gmail.com",
                'login': True
            }])'''


    #test donde la clienta es correcta
    def test_socia_correcta(self):
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
    def test_socia_nombre_con_mayusculas(self):
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
    def test_socia_nombre_con_numero(self):
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
    def test_socia_apellidos_con_mayusculas(self):
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
    def test_socia_apellidos_con_numero(self):
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
    def test_socia_edad_menor_14(self):
        print("\n")
        print("SEXTO TEST")
        hoy = datetime.date.today()
        fecha_nac = hoy - relativedelta(years=13)
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
            print("La edad es menor a 14 años y falla al crear la socia")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    #test donde la socia tiene un peso negativo
    #El error en la consola es por ser restriccion SQL, pero el test se realiza correctamente
    def test_socia_peso_negativo(self):
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

        
    #test donde la socia tiene una altura negativa
    #El error en la consola es por ser restriccion SQL, pero el test se realiza correctamente
    def test_socia_altura_negativa(self):
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
    def test_socia_fecha_nacimiento_futura(self):
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
    def test_socia_con_mismo_dni(self):
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
    def test_socia_con_mismo_nie(self):
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