from rest_framework import serializers
from .models import Job
from apps.companies.serializers import CompanySerializer

class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'description', 'salary', 'location', 'created_at', 'is_active']
        read_only_fields = ['company', 'created_at']

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Название не должен быть пустым!")
        
        if len(value) < 3:
            raise serializers.ValidationError("Название слишком короткое")

        return value
    
    
     
    def validate_salary(self, value):
        
        if value <= 0:
            raise serializers.ValidationError("Зарплата должна быть больше 0!")
        
        return value