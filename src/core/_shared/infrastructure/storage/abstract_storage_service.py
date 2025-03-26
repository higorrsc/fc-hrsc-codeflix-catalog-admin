from abc import ABC, abstractmethod


class AbstractStorageService(ABC):
    """
    Abstract base class for storage services.
    """

    @abstractmethod
    def store(self, file_path: str, content: bytes, content_type: str):
        """
        Store a file in the storage service.

        Args:
            file_path (str): The path to store the file in.
            content (bytes): The content of the file.
            content_type (str): The type of the content.

        Raises:
            NotImplementedError: If the method has not been implemented.
        """

        raise NotImplementedError
