from rest_framework import serializers
from .models import Job
from apps.companies.serializers import CompanySerializer

class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'description', 'salary', 'location', 'created_at', 'is_active']
        read_only_fields = ['company', 'created_at']

    def create(self, validate_data):
        company = self.context['company']
        return Job.objects.create(company=company, **validate_data)
    