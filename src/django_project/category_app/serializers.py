from rest_framework import serializers


class CategoryResponseSerializer(serializers.Serializer):
    """
    Serializer for category response
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoryResponseSerializer(serializers.Serializer):
    """
    Serializer for list category response
    """

    data = CategoryResponseSerializer(many=True)  # type: ignore


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


class DeleteCategoryRequestSerializer(serializers.Serializer):
    """
    Serializer for delete category request
    """

    id = serializers.UUIDField()
