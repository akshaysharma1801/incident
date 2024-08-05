from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        message = 'You do not have permission to edit this incident.'

    def has_object_permission(self, request, view, obj):
        if obj.user != request.user:
            raise PermissionDenied(self.message)
        return True