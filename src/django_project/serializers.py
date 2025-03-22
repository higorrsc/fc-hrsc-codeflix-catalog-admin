from typing import Generic, Type, TypeVar

from rest_framework import serializers

TSerializer = TypeVar(
    "TSerializer",
    bound=serializers.Serializer,
)


class ListMetaSerializer(serializers.Serializer):
    """
    Serializer for pagination meta
    """

    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()


class ListResponseSerializer(serializers.Serializer, Generic[TSerializer]):
    """
    Generic serializer for list response
    """

    data = serializers.ListSerializer(child=serializers.Serializer())  # type: ignore
    meta = ListMetaSerializer()

    def __init__(self, child_serializer: Type[TSerializer], *args, **kwargs):
        """
        Initialize the ListResponseSerializer with a child serializer.

        Args:
            child_serializer (Type[TSerializer]): The serializer class to be used for the
                items in the 'data' field.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        super().__init__(*args, **kwargs)
        self.fields["data"] = serializers.ListSerializer(child=child_serializer())


class DeleteRequestSerializer(serializers.Serializer):
    """
    Generic serializer for delete request
    """

    id = serializers.UUIDField()
