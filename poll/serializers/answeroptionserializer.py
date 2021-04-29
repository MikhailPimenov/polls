from rest_framework import serializers

from ..models import AnswerOption


class AnswerOptionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['text']
