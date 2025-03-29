from rest_framework import serializers

from src.django_project.serializers import ListResponseSerializer, SetField


class GenreResponseSerializer(serializers.Serializer):
    """
    Serializer for genre response
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListGenreResponseSerializer(ListResponseSerializer):
    """
    Serializer for list genre response
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            child_serializer=GenreResponseSerializer,
            *args,
            **kwargs,
        )


class CreateGenreRequestSerializer(serializers.Serializer):
    """
    Serializer for create genre request
    """

    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(child=serializers.UUIDField(), required=False)


class UpdateGenreRequestSerializer(serializers.Serializer):
    """
    Serializer for update genre request
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField()
    categories = SetField(child=serializers.UUIDField())
