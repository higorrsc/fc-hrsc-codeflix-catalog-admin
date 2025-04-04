from abc import ABC, abstractmethod


class AbstractAuthServiceInterface(ABC):
    """
    Abstract base class for authentication services.
    """

    @abstractmethod
    def is_authenticated(self) -> bool:
        """
        Check if the user is authenticated.

        Returns:
            bool: True if the user is authenticated, False otherwise.

        Raises:
            NotImplementedError: If the method has not been implemented.
        """

        raise NotImplementedError

    @abstractmethod
    def has_role(self, role: str) -> bool:
        """
        Check if the user has a specific role.

        Args:
            role (str): The role to be checked.

        Returns:
            bool: True if the user has the role, False otherwise.
        """

        raise NotImplementedError
