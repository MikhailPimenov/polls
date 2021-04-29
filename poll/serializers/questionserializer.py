from rest_framework import serializers

from ..models import Question
from .answeroptionserializer import AnswerOptionNestedSerializer


class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'kind',
            'answer_options',
        ]


class QuestionNestedCreateUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    text = serializers.CharField(required=False)
    kind = serializers.CharField(required=False)
    answer_options = AnswerOptionNestedSerializer(required=False, many=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'kind',
            'answer_options',
        ]
