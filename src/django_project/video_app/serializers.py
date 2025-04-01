from rest_framework import serializers

from src.core.video.domain.value_objects import ImageType
from src.core.video.domain.value_objects import MediaStatus as MediaStatusType
from src.core.video.domain.value_objects import MediaType
from src.core.video.domain.value_objects import Rating as RatingType
from src.django_project.serializers import ListResponseSerializer, SetField


class ImageTypeField(serializers.ChoiceField):
    """
    Derived ChoiceField that uses ImageType enum values as choices.
    """

    def __init__(self, **kwargs):
        """
        Initialize the ImageTypeField with choices derived from ImageType.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent ChoiceField
                initialization.
        """

        choices = [(type.name, type.value) for type in ImageType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        """
        Convert the given data into an internal value for the ImageType field.

        Args:
            data: The data to convert.

        Returns:
            ImageType: The internal value.
        """

        value = super().to_internal_value(data)
        return ImageType(value)

    def to_representation(self, value):
        """
        Convert the internal ImageType enum value to its string representation.

        Args:
            value: The internal ImageType enum value to convert.

        Returns:
            str: The string representation of the ImageType value.
        """

        return str(super().to_representation(value))


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


class MediaTypeField(serializers.ChoiceField):
    """
    Derived ChoiceField that uses MediaType enum values as choices.
    """

    def __init__(self, **kwargs):
        """
        Initialize the MediaTypeField with choices derived from MediaType.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent ChoiceField
                initialization.
        """

        choices = [(type.name, type.value) for type in MediaType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        """
        Convert the given data into an internal value for the MediaType field.

        Args:
            data: The data to convert.

        Returns:
            MediaType: The internal value.
        """

        value = super().to_internal_value(data)
        return MediaType(value)

    def to_representation(self, value):
        """
        Convert the internal MediaType enum value to its string representation.

        Args:
            value: The internal MediaType enum value to convert.

        Returns:
            str: The string representation of the MediaType value.
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


class AudioVideoMediaSerializer(serializers.Serializer):
    """
    Serializer for audio video media
    """

    name = serializers.CharField(max_length=255)
    raw_location = serializers.CharField()
    encoded_location = serializers.CharField()
    status = MediaStatusTypeField()
    media_type = MediaTypeField()
    check_sum = serializers.CharField(required=False, allow_blank=True)


class ImageMediaSerializer(serializers.Serializer):
    """
    Serializer for image media
    """

    name = serializers.CharField(max_length=255)
    location = serializers.CharField()
    image_type = ImageTypeField()
    check_sum = serializers.CharField(required=False, allow_blank=True)


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


class VideoWithMediaResponseSerializer(serializers.Serializer):
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

    banner = ImageMediaSerializer(required=False, allow_null=True)
    thumbnail = ImageMediaSerializer(required=False, allow_null=True)
    thumbnail_half = ImageMediaSerializer(required=False, allow_null=True)
    trailer = AudioVideoMediaSerializer(required=False, allow_null=True)
    video = AudioVideoMediaSerializer(required=False, allow_null=True)
