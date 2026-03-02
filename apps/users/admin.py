from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'user_type', 'is_staff', 'is_active')

    def user_type(self, obj):
        is_employer = obj.companies.exists()
        is_applicant = obj.applications.exists()

        if is_employer and is_applicant:
            return "Employer & Applicant"
        elif is_employer:
            return "Employer"
        elif is_applicant:
            return "Applicant"
        return "Regular User"
    
    user_type.short_description = "User Type"



    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('user_type',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )



    search_fields = ('email',)