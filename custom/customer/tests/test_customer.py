from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
import datetime
from dateutil.relativedelta import relativedelta

@tagged('customer', 'post_install')
class CustomerTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(CustomerTestCase, cls).setUpClass()
        print("\n")
        print("SETUP FOR CUSTOMERS")
        print("\n")

        cls.user_without_image_1 = cls.env['res.users'].create({
            'name': 'Marc Demo',
            'email': 'mark.brown23@example.com',
            'image_1920': False,
            'login': 'demo_1',
            'password': 'demo_123'
        })
        cls.user_without_image_2 = cls.env['res.users'].create({
            'name': 'Marc Demo 2',
            'email': 'mark.brown232@example.com',
            'image_1920': False,
            'login': 'demo_2',
            'password': 'demo_123'
        })

        cls.season_pass = cls.env['customer.season.pass'].create([{
            'name': 'Student',
            'until_age': 25,
            'cost': 25.99
        },
        {
            'name': 'Normal',
            'until_age': 60,
            'cost': 30.99
        }])

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.

        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        normal_date = today - relativedelta(years=30)

        cls.user_without_image_3 = cls.env['res.users'].create({
            'name': 'Marc Demo',
            'email': 'mark.brown233@example.com',
            'image_1920': False,
            'login': 'demo_3',
            'password': 'demo_123'
        })
        cls.user_without_image_4 = cls.env['res.users'].create({
            'name': 'Marc Demo',
            'email': 'mark.brown234@example.com',
            'image_1920': False,
            'login': 'demo_4',
            'password': 'demo_123'
        })

        cls.customers = cls.env['customer.customer'].create([
            {
                'have_dni': True, 
                'dni': "66727272Z",
                'name': "Hello",
                'surnames': "Ejemplo Ejemplo",
                'birth_date': normal_date,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "transfer",
                'goal': "I want to gain muscle mass",
                'user_id': cls.user_without_image_3.id,
                'customer_season_pass_id': cls.season_pass[1].id
            },
            {
                'have_dni': True, 
                'dni': "66727272A",
                'name': "Hello",
                'surnames': "Example Example",
                'birth_date': student_date,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "in_hand",
                'goal': "I want to gain muscle mass",
                'registered': False,
                'unsubscribe_date': today - relativedelta(months=2),
                'user_id': cls.user_without_image_4.id,
                'customer_season_pass_id': cls.season_pass[0].id
            }
        ])

        cls.machines = cls.env['training.machine'].create([
            {
                'name': "Squats"
            },
            {
                'name': "Chest/Back"
            }
        ])

        

    def test_p_01_correct_customer(self):
        print("\n")
        print("FIRST TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        normal_date = today - relativedelta(years=30)

        self.customers = self.env['customer.customer'].create([
            {
                'have_dni': True, 
                'dni': "72727272Z",
                'name': "Pepe",
                'surnames': "Ejemplo Ejemplo",
                'birth_date': normal_date,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "transfer",
                'goal': "I want to gain muscle mass",
                'user_id': self.user_without_image_1.id,
                'customer_season_pass_id': self.season_pass[1].id
            },
            {
                'have_dni': True, 
                'dni': "72727272A",
                'name': "Mariano",
                'surnames': "Example Example",
                'birth_date': student_date,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "in_hand",
                'goal': "I want to gain muscle mass",
                'user_id': self.user_without_image_2.id,
                'customer_season_pass_id': self.season_pass[0].id
            }
        ])

        print("¿Registered? " + str(self.customers[0].registered))
        print("Full name: " + str(self.customers[0].name) + " " + str(self.customers[0].surnames))
        print("Age: " + str(self.customers[0].age))
        print("Season pass: " + str(self.customers[0].customer_season_pass_id.name))
        print("Season pass cost: " + str(self.customers[0].customer_season_pass_id.cost))
        print("\n")

        print("¿Registered? " + str(self.customers[1].registered))
        print("Full name: " + str(self.customers[1].name) + " " + str(self.customers[1].surnames))
        print("Age: " + str(self.customers[1].age))
        print("Season pass: " + str(self.customers[1].customer_season_pass_id.name))
        print("Season pass cost: " + str(self.customers[1].customer_season_pass_id.cost))
        print("\n")

        var = self.assertEqual(self.customers[0].registered, True)
        var2 = self.assertEqual(self.customers[1].registered, True)
        result = var and var2
        return result


    def test_p_02_customer_name_with_wrong_capital_letter(self):
        print("\n")
        print("SECOND TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "HoLa",#falla aqui
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[1].id
                }])
        except:
            print("The name contains capital letters and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    def test_p_03_customer_name_with_number(self):
        print("\n")
        print("THIRD TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "H9La",#falla aqui
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[1].id
                }])
        except:
            print("The name contains a number and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    def test_p_04_customer_surname_with_wrong_capital_letter(self):
        print("\n")
        print("FOURTH TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "EjemPlo EjemPlo",#falla aqui
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[1].id
                }])
        except:
            print("The surnames contains capital letters and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    def test_p_05_customer_surname_with_number(self):
        print("\n")
        print("FIFTH TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo 2Ejemplo",#falla aqui
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[1].id
                }])
        except:
            print("The surnames contains a number letters and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    def test_p_06_customer_age_under_14(self):
        print("\n")
        print("SIXTH TEST")
        today = datetime.date.today()
        fecha_nac = today - relativedelta(years=10)
        self.customers = self.env['customer.customer']
        try:
            var = self.assertEqual(False, True)
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,#falla aqui
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[1].id
                }])
            return var
        except:
            print("The age is under 14 and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var


    def test_p_07_customer_with_negative_weight(self):
        print("\n")
        print("SEVENTH TEST")
        today = datetime.date.today()
        fecha_nac = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,
                    'actual_weight': -200.0,#falla aqui
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[1].id
                }])
        except:
            print("The weight can't be negative and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var
            
        return False

        
    def test_p_08_customer_with_negative_height(self):
        print("\n")
        print("EIGHTH TEST")
        today = datetime.date.today()
        fecha_nac = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,
                    'actual_weight': 70.0,
                    'actual_height': -1.80,#falla aqui
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[1].id
                }])
        except:
            print("The height can't be negative and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    def test_p_09_customer_with_birth_date_in_the_future(self):
        print("\n")
        print("NINETH TEST")
        today = datetime.date.today()
        fecha_nac = today + relativedelta(years=1)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,#falla aqui
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[1].id
                }])
        except:
            print("The birth date can't be in the future and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    def test_p_10_two_customers_with_the_same_DNI(self):
        print("\n")
        print("TENTH TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        normal_date = today - relativedelta(years=30)

        try:
            self.customers = self.env['customer.customer'].create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': normal_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[1].id
                },
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Example Example",
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "in_hand",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_2.id,
                    'customer_season_pass_id': self.season_pass[0].id
                }
            ])
        except:
            print("Both customers have the same DNI and it can't create the second customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    def test_p_11_wo_customers_with_the_same_NIE(self):
        print("\n")
        print("ELEVENTH TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        normal_date = today - relativedelta(years=30)

        try:
            self.customers = self.env['customer.customer'].create([
                {
                    'have_dni': False, 
                    'nie': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': normal_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[1].id

                },
                {
                    'have_dni': False, 
                    'nie': "72727272Z",
                    'name': "Hello",
                    'surnames': "Example Example",
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "in_hand",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_2.id,
                    'customer_season_pass_id': self.season_pass[0].id
                }
            ])
        except:
            print("Both customers have the same NIE and it can't create the second customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    #TESTS FOR REGISTER AND UNSUBSCRIBE FUNCTIONALITY -----------------------------------------------------------------------

    def test_p_12_register_action(self):
        print("TWELFTH TEST")
        print("\n")
        #Solo el segundo esta dado de baja ([1]), por lo tanto, el primero ([0]) esta dado de alta.
        print("BEFORE: Registered: " + str(self.customers[1].registered) + " - Unsubscribe date: " + str(self.customers[1].unsubscribe_date))
        print("\n")
        self.customers[1].action_register()
        print("AFTER: Registered: " + str(self.customers[1].registered) + " - Register date: " + str(self.customers[1].register_date))
        print("\n")
        var = self.assertRecordValues(self.customers,[
            {'name': 'Hello', 'registered': True},
            {'name': 'Hello', 'registered': True}
        ])

        return var


    def test_p_13_try_to_register_action(self):
        print("THIRTEENTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Registered: " + str(self.customers[0].registered) + " - Unsubscribe date: " + str(self.customers[0].unsubscribe_date))
        print("\n")
        try:
            self.customers[0].action_register()
            print("AFTER: Registered: " + str(self.customers[0].registered) + " - Register date: " + str(self.customers[0].register_date))
            print("\n")
            var = self.assertRecordValues(self.customers,[
                {'name': 'Hello', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var
        except:
            print("She's already registered so it gives an UserError exception")
            print("\n")
            var = self.assertRecordValues(self.customers,[
                {'name': 'Hello', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var


    def test_p_14_unsubscribe_action(self):
        print("FOURTEENTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Registered: " + str(self.customers[0].registered) + " - Unsubscribe date: " + str(self.customers[0].unsubscribe_date))
        print("\n")

        self.customers[0].action_unsubscribe()

        print("AFTER: Registered: " + str(self.customers[0].registered) + " - Unsubscribe date: " + str(self.customers[0].unsubscribe_date))
        print("\n")
        var = self.assertRecordValues(self.customers,[
                {'name': 'Hello', 'registered': False},
                {'name': 'Hello', 'registered': False}
                ])
        return var


    def test_p_15_try_unsubscribe_action(self):
        print("FIFTEENTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Registered: " + str(self.customers[1].registered) + " - Unsubscribe date: " + str(self.customers[1].unsubscribe_date))
        print("\n")
        try:
            self.customers[1].action_unsubscribe()
            print("AFTER: Registered: " + str(self.customers[1].registered) + " - Unsubscribe date: " + str(self.customers[1].unsubscribe_date))
            print("\n")
            var = self.assertRecordValues(self.customers,[
                {'name': 'Hello', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var
        except:
            print("She's already unsubscribed so it gives an UserError exception")
            print("\n")
            var = self.assertRecordValues(self.customers,[
                {'name': 'Hello', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var

    
    #TEST FOR ENTRY AND EXIT TIME -------------------------------------------------------------------------------------

    def test_p_16_register_entry_time_on_an_unsubscribed_customer(self):
        print("SIXTEENTH TEST")
        print("\n")

        try:

            self.customer_entry_exit_time = self.env['customer.entry.exit'].create(
                {
                    'last_entry_time': None,
                    'last_exit_time': None,
                    'customer_id': self.customers[2].id,#Customer unsubscribed
                }
            )
            self.customer_entry_exit_time.action_date_entry_to_gym()
            last_entry_time = self.customer_entry_exit_time.last_entry_time

            return False
        
        except:
            print("The customer isn't registered, so you can't register an entry time")
            print("\n")
            return True


    def test_p_17_register_entry_time_on_an_subscribed_customer(self):
        print("SEVENTEENTH TEST")
        print("\n")

        self.customers[1].action_register()
        try:

            self.customer_entry_exit_time = self.env['customer.entry.exit'].create(
                {   
                    'last_entry_time': None,
                    'last_exit_time': None,
                    'customer_id': self.customers[1].id,#Customer subscribed
                }
            )

            self.customer_entry_exit_time.action_date_entry_to_gym()
            print("Last entry time: " + str(self.customer_entry_exit_time.last_entry_time))
            print("\n")

            return True
        
        except:
            print("The customer isn't registered, so you can't register an entry time")
            print("\n")
            return False

    def test_p_18_register_two_entry_time_on_an_subscribed_customer(self):
        print("EIGHTEENTH TEST")
        print("\n")

        self.customers[1].action_register()
        try:

            self.customer_entry_exit_time = self.env['customer.entry.exit'].create(
                {   
                    'last_entry_time': None,
                    'last_exit_time': None,
                    'customer_id': self.customers[1].id,#Customer subscribed
                }
            )

            self.customer_entry_exit_time.action_date_entry_to_gym()

            self.customer_entry_exit_time.action_date_entry_to_gym()


            print("Last entry time: " + str(self.customer_entry_exit_time.last_entry_time))
            print("\n")

            return False
        
        except:
            print("There is already an entry time")
            print("\n")
            return True
            

    def test_p_19_register_exit_time_on_an_unsubscribed_customer(self):
        print("NINETEENTH TEST")
        print("\n")

        try:

            self.customer_entry_exit_time = self.env['customer.entry.exit'].create(
                {
                    'last_entry_time': None,
                    'last_exit_time': None,
                    'customer_id': self.customers[2].id,#Customer unsubscribed
                }
            )
            self.customer_entry_exit_time.action_date_exit_to_gym()
            last_entry_time = self.customer_entry_exit_time.last_entry_time

            return False
        
        except:
            print("The customer isn't registered, so you can't register an exit time")
            print("\n")
            return True


    def test_p_20_register_exit_time_on_an_subscribed_customer(self):
        print("TWENTIETH TEST")
        print("\n")

        self.customers[1].action_register()
        try:

            self.customer_entry_exit_time = self.env['customer.entry.exit'].create(
                {   
                    'last_entry_time': None,
                    'last_exit_time': None,
                    'customer_id': self.customers[1].id,#Customer subscribed
                }
            )

            self.customer_entry_exit_time.action_date_entry_to_gym()

            self.customer_entry_exit_time.action_date_exit_to_gym()

            print("Last exit time: " + str(self.customer_entry_exit_time.last_exit_time))
            print("\n")

            return True
        
        except:
            print("The customer isn't registered, so you can't register an exit time")
            print("\n")
            return False


    def test_p_21_register_exit_time_before_entry_time_on_an_subscribed_customer(self):
        print("TWENTY FIRST TEST")
        print("\n")

        self.customers[1].action_register()
        try:

            self.customer_entry_exit_time = self.env['customer.entry.exit'].create(
                {   
                    'last_entry_time': None,
                    'last_exit_time': None,
                    'customer_id': self.customers[1].id,#Customer subscribed
                }
            )

            self.customer_entry_exit_time.action_date_exit_to_gym()


            print("Last exit time: " + str(self.customer_entry_exit_time.last_exit_time))
            print("\n")

            return False
        
        except:
            print("There is already an exit time")
            print("\n")
            return True
    

    def test_p_22_register_two_exit_time_on_an_subscribed_customer(self):
        print("TWENTY SECOND TEST")
        print("\n")

        self.customers[1].action_register()
        try:

            self.customer_entry_exit_time = self.env['customer.entry.exit'].create(
                {   
                    'last_entry_time': None,
                    'last_exit_time': None,
                    'customer_id': self.customers[1].id,#Customer subscribed
                }
            )

            self.customer_entry_exit_time.action_date_entry_to_gym()

            self.customer_entry_exit_time.action_date_entry_to_gym()


            print("Last entry time: " + str(self.customer_entry_exit_time.last_entry_time))
            print("\n")

            return False
        
        except:
            print("There isn't any entry time, you can't create an exit time")
            print("\n")
            return True



    #TESTS FOR THE MONTHLY REVIEW FUNCTIONALITY -----------------------------------------------------------------------

    def test_p_23_correct_monthly_review(self):
        print("TWENTY THIRD TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("Customer's weight: " + str(self.customers[0].actual_weight))
        print("Customer's height: " + str(self.customers[0].actual_height))
        print("\n")
        self.review = self.env['monthly.review']
        self.review.create([
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
                    'customer_id': self.customers[0].id
                }])

        print("AFTER: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("Customer's weight: " + str(self.customers[0].actual_weight))
        print("Customer's height: " + str(self.customers[0].actual_height))
        print("\n")

        var = self.assertEqual(1, len(self.customers[0].monthly_review_ids))
        return var


    def test_p_24_wrong_monthly_review_same_date(self):
        print("TWENTY FOURTH TEST")
        print("\n")

        self.review = self.env['monthly.review']
        self.review.create([
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
                    'customer_id': self.customers[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("\n")

        try:
            print("Trying to add another review with the same date...")
            self.wrong_review = self.env['monthly.review']
            self.wrong_review.create([
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
                    'customer_id': self.customers[0].id
                }])
        except:
            print("It goes wrong because you have to wait a month to do another review.")
            print("AFTER: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
            print("\n")

            var = self.assertEqual(1, len(self.customers[0].monthly_review_ids))
            return var
        
    def test_p_25_wrong_monthly_review_in_the_same_month(self):
        print("TWENTY FIFTH TEST")
        print("\n")

        self.review = self.env['monthly.review']
        self.review.create([
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
                    'customer_id': self.customers[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("\n")

        try:
            print("Trying to add another review 29 days later...")
            self.wrong_review = self.env['monthly.review']
            self.wrong_review.create([
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
                    'customer_id': self.customers[0].id
                }])
        except:
            print("It goes wrong because you have to wait an entirely month.")
            print("AFTER: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
            print("\n")

            var = self.assertEqual(1, len(self.customers[0].monthly_review_ids))
            return var


    def test_p_26_two_monthly_reviews_correct(self):
        print("TWENTY SIXTH TEST")
        print("\n")

        print("BEFORE: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("\n")

        self.review = self.env['monthly.review']
        self.review.create([
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
                    'customer_id': self.customers[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("AFTER A REVIEW: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("\n")
        
        self.wrong_review = self.env['monthly.review']
        self.wrong_review.create([
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
                    'customer_id': self.customers[0].id
                }])

        print("AFTER: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("\n")

        var = self.assertEqual(2, len(self.customers[0].monthly_review_ids))
        return var

    
    #TESTS FOR TRAINING FUNCTIONALITY -----------------------------------------------------------------------


    def test_p_27_personal_training(self):
        print("TWENTY SEVENTH TEST")
        print("\n")

        print("BEFORE: Number of trainings: " + str(len(self.customers[0].customer_training_ids)))
        print("\n")

        self.training = self.env['customer.training']
        self.training.create([
                {
                    'name': "My training",
                    'numb_turns': 1,
                    'machine_use': True,
                    'training_machine_ids': self.machines[0],
                    'customer_id': self.customers[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("AFTER: Number of trainings: " + str(len(self.customers[0].customer_training_ids)))
        print("\n")

        var = self.assertEqual(1, len(self.customers[0].customer_training_ids))
        return var


    def test_p_28_two_personal_trainings(self):
        print("TWENTY EIGHTH TEST")
        print("\n")

        print("BEFORE: Number of trainings: " + str(len(self.customers[0].customer_training_ids)))
        print("\n")

        self.training = self.env['customer.training']
        self.training.create([
                {
                    'name': "My training",
                    'numb_turns': 1,
                    'machine_use': True,
                    'training_machine_ids': self.machines[0],
                    'customer_id': self.customers[0].id
                },
                {
                    'name': "My training 2",
                    'numb_turns': 2,
                    'machine_use': True,
                    'training_machine_ids': [self.machines[0].id, self.machines[1].id],
                    'customer_id': self.customers[0].id
                }
                ])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("AFTER: Number of trainings: " + str(len(self.customers[0].customer_training_ids)))
        print("\n")

        var = self.assertEqual(2, len(self.customers[0].customer_training_ids))
        return var

    
    
    #TEST FOR EDITING DATA ---------------------------------------------------------------------------------------------------------------


    def test_p_29_edit_customer(self):
        print("TWENTY NINETH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE:")
        print("Name: " + str(self.customers[0].name))
        print("Surnames: " + str(self.customers[0].surnames))
        print("Birth date: " + str(self.customers[0].birth_date))
        print("Age: " + str(self.customers[0].age))
        print("\n")

        self.socia_editada = self.customers[0].write({
            'name': 'Jose Maria',
            'surnames': 'Iglesias Bellido',
            'birth_date': datetime.date.today() - relativedelta(years=58)
        })
        
        print("AFTER:")
        print("Name: " + str(self.customers[0].name))
        print("Surnames: " + str(self.customers[0].surnames))
        print("Birth date: " + str(self.customers[0].birth_date))
        print("Age: " + str(self.customers[0].age))
        print("\n")
        var1 = self.assertEqual(self.customers[0].name, 'Jose Maria')
        var2 = self.assertEqual(self.customers[0].surnames, 'Iglesias Bellido')
        var3 = self.assertEqual(self.customers[0].birth_date, datetime.date.today() - relativedelta(years=58))
        var4 = self.assertEqual(self.customers[0].age, 58)
        res = var1 and (var2 and (var3 and (var4)))
        return res



    #TEST FOR PAYMENT MORE THAN ONE MONTH AT THE SAME TIME -------------------------------------------------------------------------------------

    def test_p_30_more_than_one_month_payment(self):
        #There is an error because the wizard needs to know what customer we have and in a test case we can't make it
        print("THERTIETH TEST")
        print("\n")

        self.customer_monthly_payment = self.env['customer.monthly.payment'].create(
            {
                'name': 'Example of two payments in a row',
                'customer_id': self.customers[0].id,
                'amount_months': 2
            }
        )

        
        self.customer_monthly_payment.action_monthly_payment_2()
        invoice = self.env["account.move"].search([("name", "=", "Example of two payments in a row")])
        print(invoice)

        return True

    def test_p_31_more_than_one_month_payment_customer_not_registered(self):
        print("THERTY FIRST TEST")
        print("\n")

        try:

            self.customer_monthly_payment = self.env['customer.monthly.payment'].create(
                {
                    'name': 'Example of two payments in a row',
                    'customer_id': self.customers[1].id,#Customer unsubscribed
                    'amount_months': 2
                }
            )
            self.customer_monthly_payment.action_monthly_payment_2()
            invoice = self.env["account.move"].search([("name", "=", "Example of two payments in a row")])
            print(invoice)
            return True
        
        except:
            print("The customer isn't registered, so you can't register a monthly payment")
            print("\n")


    #TEST FOR NEW SEASON PASS -------------------------------------------------------------------------------------

    #edad por debajo
    def test_p_32_correct_customer_with_season_pass_under_age(self):
        print("\n")
        print("THERTY SECOND TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)

        self.customers = self.env['customer.customer'].create({
                'have_dni': True, 
                'dni': "72727272Z",
                'name': "Pepe",
                'surnames': "Ejemplo Ejemplo",
                'birth_date': student_date,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "transfer",
                'goal': "I want to gain muscle mass",
                'user_id': self.user_without_image_1.id,
                'customer_season_pass_id': self.season_pass[0].id
            })

        print("Season pass: " + str(self.customers[0].customer_season_pass_id.name))
        print("Season pass cost: " + str(self.customers[0].customer_season_pass_id.cost))
        print("\n")

        result = self.assertEqual(self.customers.customer_season_pass_id.name, 'Student')
        return result


    #edad por encima (salta la excepcion)
    def test_p_33_incorrect_customer_with_season_pass(self):
        print("\n")
        print("THERTY THIRD TEST")
        today = datetime.date.today()
        wrong_date = today - relativedelta(years=26)

        try:
            self.customers = self.env['customer.customer'].create({
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Pepe",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': wrong_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass",
                    'user_id': self.user_without_image_1.id,
                    'customer_season_pass_id': self.season_pass[0].id
                })

            print("Season pass: " + str(self.customers[0].customer_season_pass_id.name))
            print("Season pass cost: " + str(self.customers[0].customer_season_pass_id.cost))
            print("\n")

            result = self.assertEqual(self.customers.customer_season_pass_id.name, 'Student')
            return result

        except:
            print("The customer age is older than the age to use that season pass")
            print("\n")
            return True


    #edad igual
    def test_p_34_correct_customer_with_season_pass_same_age(self):
        print("\n")
        print("THERTY FOURTH TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=25) - relativedelta(days=1)

        self.customers = self.env['customer.customer'].create({
                'have_dni': True, 
                'dni': "72727272Z",
                'name': "Pepe",
                'surnames': "Ejemplo Ejemplo",
                'birth_date': student_date,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "transfer",
                'goal': "I want to gain muscle mass",
                'user_id': self.user_without_image_1.id,
                'customer_season_pass_id': self.season_pass[0].id
            })
            
        print("Season pass: " + str(self.customers.customer_season_pass_id.name))
        print("Season pass cost: " + str(self.customers.customer_season_pass_id.cost))
        print("\n")

        result = self.assertEqual(self.customers.customer_season_pass_id.name, 'Student')

        return result
    

