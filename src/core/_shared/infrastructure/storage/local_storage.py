from pathlib import Path

from src.core._shared.infrastructure.storage.abstract_storage_service import (
    AbstractStorageService,
)


class LocalStorage(AbstractStorageService):
    """
    LocalStorage service for storing files locally.
    """

    TMP_BUCKET = "/tmp/codeflix-storage"

    def __init__(self, bucket: str = TMP_BUCKET) -> None:
        """
        Initialize the LocalStorage service.

        Args:
            bucket (str): The path to the root directory where files will be stored.
                Defaults to /tmp/codeflix-storage.
        """

        self.bucket = Path(bucket)
        if not self.bucket.exists():
            self.bucket.mkdir(parents=True)

    def store(self, file_path: str, content: bytes, content_type: str) -> None:
        """
        Store a file in the storage service.

        Args:
            file_path (str): The path to store the file in.
            content (bytes): The content of the file.
            content_type (str): The type of the content.
        """

        full_path = self.bucket / file_path
        if not full_path.parent.exists():
            full_path.parent.mkdir(parents=True)

        with open(full_path, "wb") as file:
            file.write(content)
