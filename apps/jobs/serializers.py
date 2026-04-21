from rest_framework import serializers
from .models import Job
from ..companies.models import Company
from apps.companies.serializers import CompanySerializer

class JobSerializer(serializers.ModelSerializer):
    company_detail = CompanySerializer(source='company', read_only=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), write_only=True)


    class Meta:
        model = Job
        fields = ['id', 'company', 'company_detail', 'title', 'description', 'salary', 'location', 'created_at', 'is_active']
        read_only_fields = ['id', 'company_detail','created_at']

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
    
    def validate_company(self, value):
        request = self.context['request']
        if value.owner != request.user:
            raise serializers.ValidationError(
                "Это не ваша компания"
            )
        return value