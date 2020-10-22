from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoModelPermissions


class CheckIsStaff(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

# class OnlyIsStaffAllowSeeOrder(BasePermission):
#
#     def has_permission(self, request, view):
#         return bool(
#             request.user.is_staff
#         )

class GETModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
