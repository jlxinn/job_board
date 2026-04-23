from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.jobs.models import Job
from apps.companies.models import Company

User = get_user_model()

class JobTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='user@mail.com',
            password='123456789'
        )
        self.client.force_authenticate(user=self.user)
        self.company = Company.objects.create(
            name='TestCo',
            owner=self.user,
            website=''
        )

    def test_create_job(self):
        self.client
        url = reverse('job-list')

        data = {
            'title': 'Python Dev',
            'description': 'Backend',
            'salary': 2000,
            'location': 'Japan',
            'company': self.company.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)

    def test_search_by_company_name(self):
        Job.objects.create(
            title='Backend Dev',
            description='Django',
            salary=1000,
            location='Japan',
            company=self.company
        )

        url = reverse('job-list') + '?search=testco'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_location(self): #вместе с icontains без учета к регистру
        Job.objects.create(
            title='dev',
            description='Test',
            salary=1000,
            location='Japan',
            company=self.company
        )

        url = reverse('job-list') + '?location=jap'
        response = self.client.get(url)

        self.assertEqual(len(response.data['results']), 1)

    def test_salary_range(self):
        Job.objects.create(
            title='Low',
            description='Test',
            salary=1000,
            location='Japan',
            company=self.company
        )

        Job.objects.create(
            title='High',
            description='Test',
            salary=3000,
            location='Japan',
            company=self.company
        )

        url = reverse('job-list') + '?min_salary=2000'
        response = self.client.get(url)

        self.assertEqual(len(response.data['results']), 1)

    def test_my_jobs(self):
        Job.objects.create(
            title='My Job',
            description='Test',
            salary=1000,
            location='Japan',
            company=self.company
        )

        url = reverse('job-my')
        response = self.client.get(url)

        self.assertEqual(len(response.data['results']), 1)