from rest_framework import permissions

from core.models import Reader


class IsReaderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Reader) -> bool:
        if request.user.first_name == obj.name and request.user.last_name == obj.surname:
            return True
        return False
