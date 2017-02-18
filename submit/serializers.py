from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from submit.models import SubmitReceiver


class ExternalSubmitSerializer(serializers.Serializer):
    """
    Used to deserialize and validate requests from API.
    """
    token = serializers.CharField(max_length=64)
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    score = serializers.DecimalField(max_digits=10, decimal_places=5)

    def validate_token(self, value):
        try:
            receiver = SubmitReceiver.objects.get(token=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Token does not belong to any submit receiver.')
        return value
