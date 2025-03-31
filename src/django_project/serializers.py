from typing import Generic, Type, TypeVar

from rest_framework import serializers

TSerializer = TypeVar(
    "TSerializer",
    bound=serializers.Serializer,
)


class SetField(serializers.ListField):
    """
    Serializer for set field
    """

    def to_internal_value(self, data):  # type: ignore
        """
        Override to_internal_value to convert the list of uuids to a set
        """

        return set(super().to_internal_value(data))

    def to_representation(self, data):
        """
        Override to_representation to convert the set of uuids to a list.
        """

        return list(super().to_representation(data))


class CreateResponseSerializer(serializers.Serializer):
    """
    Generic serializer for create response
    """

    id = serializers.UUIDField()


class ListMetaSerializer(serializers.Serializer):
    """
    Generic serializer for pagination meta
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


class RetrieveDeleteRequestSerializer(serializers.Serializer):
    """
    Generic serializer for retrieve and delete request
    """

    id = serializers.UUIDField()
