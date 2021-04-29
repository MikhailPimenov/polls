from rest_framework import serializers

from ..models import Poll
from .questionserializer import QuestionSerializer


class PollsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = [
            'id',
            'name',
            'description',
        ]


class PollDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = [
            'id',
            'name',
            'start_date',
            'end_date',
            'description',
            'questions',
        ]
