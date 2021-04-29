from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import serializers

from ..models import Question, UserAnswer, UserPoll
from .useranswerserializer import UserAnswerNestedCreateUpdateSerializer, UserAnswerSerializer


class UserPollDetailSerializer(serializers.ModelSerializer):
    user_answers = UserAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = UserPoll
        fields = [
            'user_id',
            'poll',
            'user_answers',
        ]


class UserPollCreateUpdateSerializer(serializers.ModelSerializer):
    user_answers = UserAnswerNestedCreateUpdateSerializer(many=True)

    class Meta:
        model = UserPoll
        fields = [
            'user_id',
            'poll',
            'user_answers',
        ]

    def create(self, validated_data):
        user_answers = validated_data.pop("user_answers")
        user_poll = UserPoll.objects.create(**validated_data)

        for user_answer in user_answers:
            try:
                question = Question.objects.get(
                    id=user_answer.get("question").get("id")
                )
            except ObjectDoesNotExist:
                user_poll.delete()
                raise Http404  # TODO: make this exception more informative

            if question.poll.id != user_poll.poll.id:
                user_poll.delete()
                raise Http404  # TODO: make this exception more informative

            UserAnswer.objects.create(
                text=user_answer.get("text"),
                user_poll=user_poll,
                question=question,
            )
        return user_poll

    def update(self, instance, validated_data):
        user_answers = validated_data.pop("user_answers")

        for user_answer in user_answers:
            try:
                question = Question.objects.get(
                    id=user_answer.get("question").get("id")
                )
            except ObjectDoesNotExist:
                raise Http404  # TODO: make this exception more informative

            if question.poll.id != instance.poll.id:
                raise Http404  # TODO: make this exception more informative

            user_answer_existing = UserAnswer.objects.get(
                user_poll=instance.id,
                question=question
            )
            user_answer_existing.text = user_answer.get("text")
            user_answer_existing.save()

        return instance
