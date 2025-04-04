import os
from typing import Dict

import jwt
from dotenv import load_dotenv

from src.core._shared.infrastructure.auth.auth_service_interface import (
    AbstractAuthServiceInterface,
)

load_dotenv()


class JwtAuthService(AbstractAuthServiceInterface):
    """
    A service for handling JWT authentication.
    This class is responsible for decoding JWT tokens and checking user roles.
    """

    def __init__(self, token: str = "") -> None:
        """
        Initialize the JwtAuthService.

        Args:
            token (str): The token to be verified, in the format of "Bearer <token>".
                Defaults to an empty string, which will not be verified.

        Raises:
            ValueError: If the AUTH_PUBLIC_KEY environment variable is not set.
        """
        raw_public_key = os.getenv("AUTH_PUBLIC_KEY")
        self.public_key = (
            f"-----BEGIN PUBLIC KEY-----\n{raw_public_key}\n-----END PUBLIC KEY-----"
            if raw_public_key
            else None
        )
        self.token = token.replace("Bearer ", "", 1) if token else None

    def _decode_token(self) -> Dict:
        """
        Decode the token and return its payload.

        Returns:
            Dict[str, Any]: The payload of the token, or an empty dictionary if the
                            token is invalid.
        """

        try:
            return jwt.decode(
                jwt=self.token,  # type: ignore
                key=self.public_key,  # type: ignore
                algorithms=["RS256"],
                audience="account",
            )
        except jwt.PyJWTError:
            return {}

    def is_authenticated(self) -> bool:
        """
        Check if the user is authenticated.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """

        return bool(self._decode_token())

    def has_role(self, role: str) -> bool:
        """
        Check if the user has a specific role.

        Args:
            role (str): The role to be checked.

        Returns:
            bool: True if the user has the role, False otherwise.
        """

        return role in self._decode_token().get("realm_access", {}).get("roles", [])
