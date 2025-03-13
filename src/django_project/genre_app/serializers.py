from rest_framework import serializers


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


class CreateGenreRequestSerializer(serializers.Serializer):
    """
    Serializer for create genre request
    """

    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(child=serializers.UUIDField(), required=False)


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
    categories = SetField(child=serializers.UUIDField())


class DeleteGenreRequestSerializer(serializers.Serializer):
    """
    Serializer for delete genre request
    """

    id = serializers.UUIDField()
