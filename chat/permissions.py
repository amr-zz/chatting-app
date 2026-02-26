from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'conversation_created_by'):
            return obj.conversation_created_by == request.user
        return obj.owner == request.user