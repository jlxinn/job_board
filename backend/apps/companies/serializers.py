from rest_framework import serializers
from .models import Company
#from apps.jobs.serializers import JobSerializer

class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    #jobs = JobSerializer(read_only=True)
    website = serializers.URLField(allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'website', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at',]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Название не должен быть пустым!")
    
        if value.isdigit():
            raise serializers.ValidationError("Название не может состоять только из цифр!")
        
        if len(value) < 3:
            raise serializers.ValidationError("Название слишком короткое!")
        
        queryset = Company.objects.filter(name__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Компания с таким названием уже существует!")
        
        return value
    
    def get_owner(self, obj):
        if obj.owner:
            return {
                'id': obj.owner.id,
                'email': obj.owner.email
            }
        return None