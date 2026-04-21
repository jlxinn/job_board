from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCompanyOwner(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "POST":
            return user.user_type in ['Employer', 'Regular User', 'Employer & Applicant']
        
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user