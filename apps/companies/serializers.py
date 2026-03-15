from rest_framework import serializers
from .models import Company
#from apps.jobs.serializers import JobSerializer

class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    #jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'website', 'owner', 'created_at', 'updated_at',]
        read_only_fields = ['owner', 'created_at', 'updated_at',]