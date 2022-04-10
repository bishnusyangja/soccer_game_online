from rest_framework.permissions import BasePermission


class StaffPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff


class PublicPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous