from rest_framework import serializers


class GenreResponseSerializer(serializers.Serializer):
    """
    Serializer for genre response
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListGenreResponseSerializer(serializers.Serializer):
    """
    Serializer for list genre response
    """

    data = GenreResponseSerializer(many=True)  # type: ignore


class RetrieveGenreResponseSerializer(serializers.Serializer):
    """
    Serializer for retrieve genre response
    """

    data = GenreResponseSerializer(source="*")  # type: ignore


class RetrieveGenreRequestSerializer(serializers.Serializer):
    """
    Serializer for retrieve genre request
    """

    id = serializers.UUIDField()


class CreateGenreRequestSerializer(serializers.Serializer):
    """
    Serializer for create genre request
    """

    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField(default=True)
    categories = serializers.ListField(child=serializers.UUIDField())


class CreateGenreResponseSerializer(serializers.Serializer):
    """
    Serializer for create genre response
    """

    id = serializers.UUIDField()


class UpdateGenreRequestSerializer(serializers.Serializer):
    """
    Serializer for update genre request
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class DeleteGenreRequestSerializer(serializers.Serializer):
    """
    Serializer for delete genre request
    """

    id = serializers.UUIDField()
