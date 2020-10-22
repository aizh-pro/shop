from rest_framework.permissions import BasePermission, SAFE_METHODS


class CheckIsStaff(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class OnlyIsStaffAllowSeeOrder(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_staff
        )

