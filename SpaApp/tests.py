from datetime import timedelta, date
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Product, ProductDelivery, Storage, Appointment, Client
from .forms import ProductDeliveryForm

class ProductModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.code = '123'
        cls.name = 'Product'
        cls.price = 123
        cls.expiry_duration = timedelta(days=123)
        cls.test_product = Product.objects.create(
            code=cls.code,
            name=cls.name,
            price=cls.price,
            expiry_duration=cls.expiry_duration,
        )

    def tearDown(self):
        self.product.delete()
        self.test_product.delete()

    def setUp(self):
        self.product = Product.objects.get(code='123')

    def test_product_fields(self):
        self.assertEqual(self.product.code, self.code)
        self.assertEqual(self.product.name, self.name)
        self.assertEqual(self.product.price, self.price)
        self.assertEqual(self.product.expiry_duration, self.expiry_duration)
        self.assertEqual(self.product.deficit_status, False)

    def test_max_values(self):
        code_max_length = self.product._meta.get_field('code').max_length
        name_max_length = self.product._meta.get_field('name').max_length
        self.assertEqual(code_max_length, 50)
        self.assertEqual(name_max_length, 100)


class ProductDeliveryModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_product = Product.objects.create(
            code='123',
            name='Product',
            price=123,
            expiry_duration=timedelta(days=123),
        )
        cls.name = 'Product'
        cls.amount = 123
        cls.date = date.today()

        cls.test_delivery = ProductDelivery.objects.create(
            name=cls.name,
            amount=cls.amount,
            date=cls.date,
        )

    def tearDown(self) -> None:
        self.test_product.delete()
        self.test_delivery.delete()

    def setUp(self) -> None:
        self.delivery = ProductDelivery.objects.get(name=self.name)

    def test_delivery_fields(self):
        self.assertEqual(self.delivery.name, self.name)
        self.assertEqual(self.delivery.amount, self.amount)
        self.assertEqual(self.delivery.date, self.date)

    def test_max_values(self):
        name_max_length = self.delivery._meta.get_field('name').max_length
        self.assertEqual(name_max_length, 100)


class StorageModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_product = Product.objects.create(
            code='123',
            name='Product',
            price=123,
            expiry_duration=timedelta(days=123),
        )

        cls.test_delivery = ProductDelivery.objects.create(
            name='Product',
            amount=123,
            date=date.today(),
        )

    def tearDown(self) -> None:
        self.test_product.delete()
        self.test_delivery.delete()

    def setUp(self) -> None:
        self.storage = Storage.objects.get(product=self.test_product.code)

    def test_storage_fields(self):
        self.assertEqual(self.storage.product, self.test_product)
        self.assertEqual(self.storage.delivery, self.test_delivery)


class HomePageTestCase(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_contains_correct_html(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, '<title>Beauty Salon</title>')
        self.assertContains(response, '<h1 class="header">WITAMY W SPA</h1>')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

    def test_navbar_exists(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, '<nav class="navbar navbar-expand-lg" style="background-color: #FFB6C1;">')

    def test_footer_exists(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, '<footer class="bg-light text-center text-lg-start">')


class OwnerPageTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password, first_name='test',
                                             last_name='test', email='kapit2000@gmail.com')

    def test_owner_page_status_code(self):
        url = reverse('owner_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class StorageAlertTestCase(TestCase):
    """Tests three products.

    Product 1 - Not expired
    Product 2 - Soon to be expired
    Product 3 - Expired
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(username='testuser',
                                            email='testuser@test.com',
                                            first_name='test',
                                            last_name='user',
                                            password='testpass',
                                            is_active=True,
                                            type=User.Types.OWNER
                                            )

        cls.product1 = Product.objects.create(code="PR1",
                                              name='Product 1',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=21))
        cls.delivery1 = ProductDelivery.objects.create(name="Product 1",
                                                       amount=10,
                                                       date=date.today())
        cls.storage1 = Storage.objects.get(product=cls.product1,
                                           delivery=cls.delivery1)

        cls.product2 = Product.objects.create(code="PR2",
                                              name='Product 2',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=6))
        cls.delivery2 = ProductDelivery.objects.create(name="Product 2",
                                                       amount=20,
                                                       date=date.today())
        cls.storage2 = Storage.objects.get(product=cls.product2,
                                           delivery=cls.delivery2)

        cls.product3 = Product.objects.create(code="PR3",
                                              name='Product 3',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=7))
        cls.delivery3 = ProductDelivery.objects.create(name="Product 3",
                                                       amount=30,
                                                       date=date.today() - timedelta(days=14))
        cls.storage3 = Storage.objects.get(product=cls.product3,
                                           delivery=cls.delivery3)

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def tearDown(self):
        self.storage1.delete()
        self.storage2.delete()
        self.storage3.delete()
        self.product1.delete()
        self.product2.delete()
        self.product3.delete()
        self.delivery1.delete()
        self.delivery2.delete()
        self.delivery3.delete()
        self.user.delete()

    def test_owner_page_with_no_expired_or_soon_to_expire_products(self):
        response = self.client.get(reverse('owner_page'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Product 1')

    def test_owner_page_with_soon_to_be_expired_products(self):
        response = self.client.get(reverse('owner_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Warning!')
        self.assertContains(response, 'Following products have less than a week:')
        self.assertContains(response, 'Product 2')

    def test_owner_page_with_expired_products(self):
        response = self.client.get(reverse('owner_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Warning!')
        self.assertContains(response, 'Following products have expired:')
        self.assertContains(response, 'Product 3')


class ScheduleViewTestCase(TestCase):
    def setUp(self):
        self.client1 = Client.objects.create(name='John', surname='Doe', phone_number='123456789')
        self.appointment1 = Appointment.objects.create(name='Meeting', date='2023-04-23', time='14:00', client=self.client1)
        

    # def test_schedule_view(self):
    #     url = reverse('schedule')
    #     response = self.client.get(url)
    #     self.assertContains(response, self.appointment1.client.name)
    #     self.assertContains(response, '<td>April 23, 2023</td>')
    #     self.assertContains(response, '<td>2 p.m.</td>')
        

class AppointmentTemplateTest(TestCase):
    def setUp(self):
        self.client1 = Client.objects.create(name='John', surname='Doe', phone_number='123456789')
        self.appointment1 = Appointment.objects.create(name='Meeting', description='Discuss new project', date='2023-04-23', time='14:00', client=self.client1)

    def test_appointment_template(self):
        url = reverse('appointment', args=[self.appointment1.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'appointment.html')
        self.assertContains(response, self.appointment1.name)
        self.assertContains(response, self.appointment1.description)
        self.assertContains(response, '<dd>April 23, 2023</dd>')
        self.assertContains(response, '<dd>2 p.m.</dd>')
        self.assertContains(response, self.client1)


class ProductDeliveryTest(TestCase):
 
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.product1 = Product.objects.create(code="PR1",
                                              name='Product 1',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=21))
        cls.delivery1 = ProductDelivery.objects.create(name="Product 1",
                                                       amount=10,
                                                       date=date.today())
        cls.storage1 = Storage.objects.get(product=cls.product1,
                                           delivery=cls.delivery1)

        cls.product2 = Product.objects.create(code="PR2",
                                              name='Product 2',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=6))
        cls.delivery2 = ProductDelivery.objects.create(name="Product 2",
                                                       amount=20,
                                                       date=date.today())
        cls.storage2 = Storage.objects.get(product=cls.product2,
                                           delivery=cls.delivery2)

        cls.product3 = Product.objects.create(code="PR3",
                                              name='Product 3',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=7))
        cls.delivery3 = ProductDelivery.objects.create(name="Product 3",
                                                       amount=30,
                                                       date=date.today() - timedelta(days=14))
        cls.storage3 = Storage.objects.get(product=cls.product3,
                                           delivery=cls.delivery3)

    def setUp(self):
        self.client.login(username='testuser', password='testpass')
        self.form_data = {
            'name': self.product1.name,
            'amount': 10,
            'expiry_duration': date.today()
        }

    def tearDown(self):
        self.storage1.delete()
        self.storage2.delete()
        self.storage3.delete()
        self.product1.delete()
        self.product2.delete()
        self.product3.delete()
        self.delivery1.delete()
        self.delivery2.delete()
        self.delivery3.delete()

    def test_get_delivery_page(self):
        response = self.client.get(reverse('delivery_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delivery_page.html')
        self.assertIsInstance(response.context['form'], ProductDeliveryForm)

    def test_post_valid_form(self):
        response = self.client.post(reverse('delivery_page'), data=self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductDelivery.objects.count(), 8)
        response = self.client.post(reverse('delivery_page'), data=self.form_data)
        self.assertEqual(response.status_code, 200)
        

class ProductListViewTests(TestCase):
 
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.product1 = Product.objects.create(code="PR1",
                                              name='Product 1',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=21))
        cls.delivery1 = ProductDelivery.objects.create(name="Product 1",
                                                       amount=10,
                                                       date=date.today())
        cls.storage1 = Storage.objects.get(product=cls.product1,
                                           delivery=cls.delivery1)

        cls.product2 = Product.objects.create(code="PR2",
                                              name='Product 2',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=6))
        cls.delivery2 = ProductDelivery.objects.create(name="Product 2",
                                                       amount=20,
                                                       date=date.today())
        cls.storage2 = Storage.objects.get(product=cls.product2,
                                           delivery=cls.delivery2)

        cls.product3 = Product.objects.create(code="PR3",
                                              name='Product 3',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=7))
        cls.delivery3 = ProductDelivery.objects.create(name="Product 3",
                                                       amount=30,
                                                       date=date.today() - timedelta(days=14))
        cls.storage3 = Storage.objects.get(product=cls.product3,
                                           delivery=cls.delivery3)

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def tearDown(self):
        self.storage1.delete()
        self.storage2.delete()
        self.storage3.delete()
        self.product1.delete()
        self.product2.delete()
        self.product3.delete()
        self.delivery1.delete()
        self.delivery2.delete()
        self.delivery3.delete()


class ProductDeliveryTest(TestCase):
 
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.product1 = Product.objects.create(code="PR1",
                                              name='Product 1',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=21))
        cls.delivery1 = ProductDelivery.objects.create(name="Product 1",
                                                       amount=10,
                                                       date=date.today())
        cls.storage1 = Storage.objects.get(product=cls.product1,
                                           delivery=cls.delivery1)

        cls.product2 = Product.objects.create(code="PR2",
                                              name='Product 2',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=6))
        cls.delivery2 = ProductDelivery.objects.create(name="Product 2",
                                                       amount=20,
                                                       date=date.today())
        cls.storage2 = Storage.objects.get(product=cls.product2,
                                           delivery=cls.delivery2)

        cls.product3 = Product.objects.create(code="PR3",
                                              name='Product 3',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=7))
        cls.delivery3 = ProductDelivery.objects.create(name="Product 3",
                                                       amount=30,
                                                       date=date.today() - timedelta(days=14))
        cls.storage3 = Storage.objects.get(product=cls.product3,
                                           delivery=cls.delivery3)

    def setUp(self):
        self.client.login(username='testuser', password='testpass')
        self.form_data = {
            'name': self.product1.name,
            'amount': 10,
            'expiry_duration': date.today()
        }

    def tearDown(self):
        self.storage1.delete()
        self.storage2.delete()
        self.storage3.delete()
        self.product1.delete()
        self.product2.delete()
        self.product3.delete()
        self.delivery1.delete()
        self.delivery2.delete()
        self.delivery3.delete()

    def test_get_delivery_page(self):
        response = self.client.get(reverse('delivery_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delivery_page.html')
        self.assertIsInstance(response.context['form'], ProductDeliveryForm)

    def test_post_valid_form(self):
        response = self.client.post(reverse('delivery_page'), data=self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductDelivery.objects.count(), 8)
        response = self.client.post(reverse('delivery_page'), data=self.form_data)
        self.assertEqual(response.status_code, 200)

    def test_amount_validation(self):
        form = ProductDeliveryForm(data={
            'name': 'Product 1',
            'amount': -10,
            'date': '2023-05-07'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['amount'], ['Ilość produktów musi być większa od 0.'])

        form = ProductDeliveryForm(data={
            'name': 'Product 1',
            'amount': 10,
            'date': '2023-05-07'
        })
        self.assertTrue(form.is_valid())
        


class ServiceListViewTests(TestCase):
 
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.product1 = Product.objects.create(code="PR1",
                                              name='Product 1',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=21))
        cls.delivery1 = ProductDelivery.objects.create(name="Product 1",
                                                       amount=10,
                                                       date=date.today())
        cls.storage1 = Storage.objects.get(product=cls.product1,
                                           delivery=cls.delivery1)

        cls.product2 = Product.objects.create(code="PR2",
                                              name='Product 2',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=6))
        cls.delivery2 = ProductDelivery.objects.create(name="Product 2",
                                                       amount=20,
                                                       date=date.today())
        cls.storage2 = Storage.objects.get(product=cls.product2,
                                           delivery=cls.delivery2)

        cls.product3 = Product.objects.create(code="PR3",
                                              name='Product 3',
                                              image=None,
                                              price=1.,
                                              expiry_duration=timedelta(days=7))
        cls.delivery3 = ProductDelivery.objects.create(name="Product 3",
                                                       amount=30,
                                                       date=date.today() - timedelta(days=14))
        cls.storage3 = Storage.objects.get(product=cls.product3,
                                           delivery=cls.delivery3)

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def tearDown(self):
        self.storage1.delete()
        self.storage2.delete()
        self.storage3.delete()
        self.product1.delete()
        self.product2.delete()
        self.product3.delete()
        self.delivery1.delete()
        self.delivery2.delete()
        self.delivery3.delete()
