from rest_framework import serializers

from src.django_project.serializers import ListResponseSerializer


class CategoryResponseSerializer(serializers.Serializer):
    """
    Serializer for category response
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoryResponseSerializer(ListResponseSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(
            child_serializer=CategoryResponseSerializer,
            *args,
            **kwargs,
        )


class RetrieveCategoryResponseSerializer(serializers.Serializer):
    """
    Serializer for retrieve category response
    """

    data = CategoryResponseSerializer(source="*")  # type: ignore


class RetrieveCategoryRequestSerializer(serializers.Serializer):
    """
    Serializer for retrieve category request
    """

    id = serializers.UUIDField()


class CreateCategoryRequestSerializer(serializers.Serializer):
    """
    Serializer for create category request
    """

    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField(default=True)


class CreateCategoryResponseSerializer(serializers.Serializer):
    """
    Serializer for create category response
    """

    id = serializers.UUIDField()


class UpdateCategoryRequestSerializer(serializers.Serializer):
    """
    Serializer for update category request
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField()
