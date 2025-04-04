from rest_framework.permissions import BasePermission

from src.core._shared.infrastructure.auth.jwt_auth_service import JwtAuthService


class IsAuthenticated(BasePermission):
    """
    Custom permission to check if the user is authenticated.
    This permission checks if the user is authenticated by verifying the JWT token
    provided in the request headers.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated.

        Args:
            request: The request object
            view: The view object

        Returns:
            bool: True if the user is authenticated, False otherwise
        """

        token = request.headers.get("Authorization")
        return JwtAuthService(token=token).is_authenticated()


class IsAdmin(BasePermission):
    """
    Custom permission to check if the user is an admin.
    This permission checks if the user has the role of "admin" by verifying the JWT token
    provided in the request headers.
    """

    def has_permission(self, request, view):
        """
        Check if the user is an admin.

        Args:
            request (Request): The incoming request.
            view (View): The view being accessed.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """

        token = request.headers.get("Authorization")
        return JwtAuthService(token=token).has_role("admin")
