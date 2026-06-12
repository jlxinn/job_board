from rest_framework import serializers
from .models import Application
from apps.jobs.models import Job
from apps.jobs.serializers import JobSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    job_detail = JobSerializer(source='job', read_only=True)
    resume = serializers.FileField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'cover_letter', 'resume', 'status', 'created_at', 'job_detail']
        read_only_fields = ['applicant', 'status', 'created_at']

    def validate(self, data):
        user = self.context["request"].user
        job = data.get("job")

        if job.company.owner == user:
            raise serializers.ValidationError("Нельзя откликаться на свою вакансию")
        
        if Application.objects.filter(applicant=user, job=job).exists():
            raise serializers.ValidationError("Вы уже откликались")
        
        return data

    def validate_status(self, value):
        instance = self.instance

        if not instance:
            return value
    
        if instance.status != "pending":
            raise serializers.ValidationError("Статус уже финальный")
        
        return value
    
    def validate_resume(self, value):
        if not value:
            return None
        return value
    
    def to_internal_value(self, data):
        data = data.copy()
        if data.get("resume") == "":
            data.pop("resume")
        return super().to_internal_value(data)
    


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ['status']
        extra_kwargs = {
            'status': {
                'help_text': 'Новый статус отклика',
                'choices': ['accepted', 'rejected']
            }
        }

    def validate_status(self, value):
        instance = self.instance

        if instance.status != 'pending':
            raise serializers.ValidationError('Статус уже финальный')
        
        return value