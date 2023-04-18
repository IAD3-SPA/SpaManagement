from django.test import TestCase
from django.urls import reverse
from .models import User

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
        self.user = User.objects.create_user(username=self.username, password=self.password, first_name='test', last_name='test', email='kapit2000@gmail.com')

    def test_owner_page_status_code(self):
        url = reverse('owner_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    

    
