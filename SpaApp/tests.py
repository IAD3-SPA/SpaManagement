import re
from datetime import timedelta, date

from django.test import TestCase, Client
from django.urls import reverse

from .models import User, Product, ProductDelivery, Storage


# Create your tests here.


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
