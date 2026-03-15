from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCompanyOwner(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "POST":
            return "Employer" in user.user_type or "Regular User" in user.user_type or "Employer & Applicant" in user.user_type
        
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user