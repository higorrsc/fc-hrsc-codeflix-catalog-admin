from rest_framework import serializers

from src.core.video.domain.value_objects import MediaStatus as MediaStatusType
from src.core.video.domain.value_objects import Rating as RatingType
from src.django_project.serializers import ListResponseSerializer, SetField


class MediaStatusTypeField(serializers.ChoiceField):
    """
    Derived ChoiceField that uses MediaStatusType enum values as choices.
    """

    def __init__(self, **kwargs):
        """
        Initialize the MediaStatusTypeField with choices derived from MediaStatusType.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent ChoiceField
                initialization.
        """

        choices = [(type.name, type.value) for type in MediaStatusType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        """
        Convert the given data into an internal value for the MediaStatusType field.

        Args:
            data: The data to convert.

        Returns:
            MediaStatusType: The internal value.
        """

        value = super().to_internal_value(data)
        return MediaStatusType(value)

    def to_representation(self, value):
        """
        Convert the internal MediaStatusType enum value to its string representation.

        Args:
            value: The internal MediaStatusType enum value to convert.

        Returns:
            str: The string representation of the MediaStatusType value.
        """

        return str(super().to_representation(value))


class RatingTypeField(serializers.ChoiceField):
    """
    Derived ChoiceField that uses RatingType enum values as choices.
    """

    def __init__(self, **kwargs):
        """
        Initialize the RatingTypeField with choices derived from RatingType.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent ChoiceField
                initialization.
        """

        choices = [(type.name, type.value) for type in RatingType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        """
        Convert the given data into an internal value for the RatingType field.

        Args:
            data: The data to convert.

        Returns:
            RatingType: The internal value.
        """

        value = super().to_internal_value(data)
        return RatingType(value)

    def to_representation(self, value):
        """
        Convert the internal RatingType enum value to its string representation.

        Args:
            value: The internal RatingType enum value to convert.

        Returns:
            str: The string representation of the RatingType value.
        """

        return str(super().to_representation(value))


class VideoWithoutMediaRequestSerializer(serializers.Serializer):
    """
    Serializer for video request
    """

    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=5, decimal_places=2)
    published = serializers.BooleanField(default=False)
    rating = RatingTypeField()

    categories = SetField(child=serializers.UUIDField())
    genres = SetField(child=serializers.UUIDField())
    cast_members = SetField(child=serializers.UUIDField())


class VideoWithoutMediaResponseSerializer(serializers.Serializer):
    """
    Serializer for video response
    """

    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=5, decimal_places=2)
    published = serializers.BooleanField()
    rating = RatingTypeField()

    categories = SetField(child=serializers.UUIDField())
    genres = SetField(child=serializers.UUIDField())
    cast_members = SetField(child=serializers.UUIDField())


class ListVideoWithoutMediaResponseSerializer(ListResponseSerializer):
    """
    Serializer for list video response
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            child_serializer=VideoWithoutMediaResponseSerializer,
            *args,
            **kwargs,
        )


class UpdateVideoWithoutMediaRequestSerializer(serializers.Serializer):
    """
    Serializer for update video request
    """

    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=5, decimal_places=2)
    published = serializers.BooleanField()
    rating = RatingTypeField()

    categories = SetField(child=serializers.UUIDField())
    genres = SetField(child=serializers.UUIDField())
    cast_members = SetField(child=serializers.UUIDField())
