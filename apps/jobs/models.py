from django.db import models

class Job(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, default='Нет значения')

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=["location"])
        ]

    def __str__(self):
        return self.title