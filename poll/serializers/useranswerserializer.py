from rest_framework import serializers

from ..models import UserAnswer
from .questionserializer import QuestionNestedCreateUpdateSerializer, QuestionSerializer


class UserAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = UserAnswer
        fields = [
            'id',
            'question',
            'text',
        ]


class UserAnswerNestedCreateUpdateSerializer(serializers.ModelSerializer):
    question = QuestionNestedCreateUpdateSerializer(required=False)

    class Meta:
        model = UserAnswer
        fields = [
            'question',
            'text',
        ]
