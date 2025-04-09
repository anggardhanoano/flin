from rest_framework.permissions import BasePermission


class IsInternalTeamOnly(BasePermission):
    """
    Allows access only to authenticated users who has internal tool access.
    """

    message = {"forbidden": "Only Internal Staff Can Access this Site"}

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
