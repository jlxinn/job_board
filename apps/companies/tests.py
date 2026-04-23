from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.companies.models import Company

User = get_user_model()

class CompanyTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='user@mail.com',
            password='123456789'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_create_company(self):
        url = reverse('company-list')

        data = {
            'name': 'Test Company apps',
            'description': 'Desc'
        }

        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.first().owner, self.user)

    def test_my_companies(self):
        Company.objects.create(name='A', owner=self.user)
        Company.objects.create(name='B', owner=self.user)

        url = reverse('company-my')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
