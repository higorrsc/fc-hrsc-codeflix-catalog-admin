import os

import pytest
from rest_framework.test import APIClient

from src.core._shared.infrastructure.auth.jwt_token_generator import JwtTokenGenerator


@pytest.fixture(scope="session", autouse=True)
def setup_auth_env():
    """
    Sets up the authentication environment for the tests by generating a fake
    public key and saving it to the environment variable AUTH_PUBLIC_KEY.

    This fixture is marked as autouse=True, which means it will be executed
    automatically before all tests. It is also marked as scope="session", which
    means that it will only be executed once per test session.

    Returns:
        JwtTokenGenerator: The instance of JwtTokenGenerator used to generate the
            fake public key.
    """

    fake_auth = JwtTokenGenerator()
    os.environ["AUTH_PUBLIC_KEY"] = (
        fake_auth.public_key_pem.decode()
        .replace("-----BEGIN PUBLIC KEY-----\n", "")
        .replace("\n-----END PUBLIC KEY-----\n", "")
    )
    return fake_auth


@pytest.fixture
def auth_token(setup_auth_env):
    """
    Generates a JWT token with the specified user information and
    expiration time.

    Returns:
        str: The encoded JWT token.
    """

    return setup_auth_env.generate_token(
        user_info={
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "realm_roles": [
                "offline_access",
                "admin",
                "uma_authorization",
                "default-roles-codeflix",
            ],
            "resource_roles": [
                "manage-account",
                "view-profile",
            ],
        }
    )


@pytest.fixture
def api_client_with_auth(auth_token):
    """
    Fixture for an API client with authentication.

    Returns:
        APIClient: An instance of the APIClient with the provided authentication token.
    """

    return APIClient(
        headers={
            "Authorization": f"Bearer {auth_token}",
        }
    )
