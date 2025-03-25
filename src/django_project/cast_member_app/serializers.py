from rest_framework import serializers

from src.core.cast_member.domain.cast_member import CastMemberType
from src.django_project.serializers import ListResponseSerializer


class CastMemberTypeField(serializers.ChoiceField):
    """
    Derived ChoiceField that uses CastMemberType enum values as choices.
    """

    def __init__(self, **kwargs):
        """
        Initialize the CastMemberTypeField with choices derived from CastMemberType.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent ChoiceField
                initialization.
        """

        choices = [(type.name, type.value) for type in CastMemberType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        """
        Convert the given data into an internal value for the CastMemberType field.

        The internal value is a CastMemberType enum value.

        Args:
            data: The data to convert.

        Returns:
            CastMemberType: The internal value.
        """

        return CastMemberType(super().to_internal_value(data))

    def to_representation(self, value):
        """
        Convert the internal CastMemberType enum value to its string representation.

        Args:
            value: The internal CastMemberType enum value to convert.

        Returns:
            str: The string representation of the CastMemberType value.
        """

        return str(super().to_representation(value))


class CastMemberResponseSerializer(serializers.Serializer):
    """
    Serializer for cast member
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField(required=True)


class ListCastMemberResponseSerializer(ListResponseSerializer):
    """
    Serializer for list cast member response
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            child_serializer=CastMemberResponseSerializer,
            *args,
            **kwargs,
        )


class CreateCastMemberRequestSerializer(serializers.Serializer):
    """
    Serializer for cast member request
    """

    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField(required=True)


class UpdateCastMemberRequestSerializer(serializers.Serializer):
    """
    Serializer for update cast member request
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField(required=True)
