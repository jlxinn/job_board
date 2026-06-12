from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.applications.models import Application
from apps.jobs.models import Job
from apps.companies.models import Company

User = get_user_model()

class ApplicationTests(APITestCase):

    def setUp(self):
        self.employer = User.objects.create_user(
            email='emp@mail.com',
            password='123456789'
        )

        self.candidate = User.objects.create_user(
            email='cand@mail.com',
            password='123456789'
        )

        self.both_user = User.objects.create_user(
            email='both@mail.com',
            password='123456789'
        )

        self.company = Company.objects.create(
            name='TestCo',
            owner=self.employer
        )

        self.job = Job.objects.create(
            title='Dev',
            description='Test',
            salary=1000,
            location='Japan',
            company=self.company
        )

        self.both_company = Company.objects.create(
            name='BothCo',
            owner=self.both_user
        )

        self.both_job = Job.objects.create(
            title='Both Dev',
            description='Test',
            salary=2000,
            location='Japan',
            company=self.both_company
        )

    def test_apply_to_job(self):
        self.client.force_authenticate(user=self.candidate)

        url = reverse('application-list')

        data = {
            'job': self.job.id,
            'cover_letter': 'Privet'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

    def test_my_applications(self):
        Application.objects.create(
            applicant=self.candidate,
            job=self.job,
            cover_letter='Test'
        )

        self.client.force_authenticate(user=self.candidate)

        url = reverse('application-my')
        response = self.client.get(url)

        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_applications_incoming(self):
        Application.objects.create(
            applicant=self.candidate,
            job=self.job,
            cover_letter='Test'
        )

        self.client.force_authenticate(user=self.employer)

        url = reverse('application-incoming')
        response = self.client.get(url)

        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_both_roles(self):

        Application.objects.create(
            applicant=self.both_user,
            job=self.both_job,
            cover_letter='TEST'
        )

        self.client.force_authenticate(user=self.both_user)
        
        my_resp = self.client.get(reverse('application-my'))
        incoming_resp = self.client.get(reverse('application-incoming'))

        self.assertEqual(len(my_resp.data['results']), 1)
        self.assertEqual(len(incoming_resp.data['results']), 1)

    def test_filter_status(self):
        Application.objects.create(
            applicant=self.candidate,
            job=self.job,
            status='pending',
            cover_letter='Test'
        )

        Application.objects.create(
            applicant=self.candidate,
            job=self.both_job,
            status='accepted',
            cover_letter='Test 2'
        )

        self.client.force_authenticate(user=self.employer)

        url = reverse('application-incoming') + '?status=pending'
        response = self.client.get(url, {'status': 'pending'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'pending')