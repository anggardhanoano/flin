from rest_framework import serializers

from commons.exceptions import ValidationErrorException


class ReadOnlySerializer(serializers.Serializer):
    def create(self, validated_data):
        raise ValidationErrorException(message="create is not allowed.")

    def update(self, instance, validated_data):
        raise ValidationErrorException(message="update is not allowed.")

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            not_allowed = set(exclude)
            for exclude_name in not_allowed:
                self.fields.pop(exclude_name)


class ErrorSerializer(ReadOnlySerializer):
    class ErrorDetailSerializer(ReadOnlySerializer):
        error_message = serializers.CharField()
        code = serializers.CharField(
            allow_null=True, allow_blank=True, default=None)
        validation_error = serializers.DictField(allow_null=True, default=None)

    errors = ErrorDetailSerializer()


class StatusSerializer(ReadOnlySerializer):
    status = serializers.CharField(default="ok", initial="ok")


class MessageSerializer(ReadOnlySerializer):
    message = serializers.CharField()


class BaseSerializerDecimalField(serializers.DecimalField):
    def __init__(self, **kwargs):
        super().__init__(
            max_digits=14, decimal_places=0, coerce_to_string=False, **kwargs
        )


class BasePaginationSerializer(ReadOnlySerializer):
    count_items = serializers.IntegerField()
    next_page = serializers.IntegerField(allow_null=True)
    previous_page = serializers.IntegerField(allow_null=True)
