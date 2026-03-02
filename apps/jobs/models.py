from django.db import models

class Job(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    