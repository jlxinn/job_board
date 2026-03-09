from rest_framework import serializers
from .models import Company
from jobs.serializers import JobSerializer

class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'website', 'owner', 'created_at', 'updated_at', 'jobs']
        read_only_fields = ['owner', 'created_at', 'updated_at', 'jobs']

        def create(self, validate_data):
            user = self.contex['request'].user
            company = Company.objects.create(owner=user, **validate_data)
            return company