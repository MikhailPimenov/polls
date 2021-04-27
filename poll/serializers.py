from rest_framework import serializers

from .models import AnswerOption, Poll, Question, UserAnswer, UserPoll


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['text', 'question']


class AnswerOptionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['text']


class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionShortSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'poll', 'kind', 'answer_options']


class QuestionShortSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionShortSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'kind', 'answer_options']


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionShortSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'start_date', 'end_date', 'description', 'questions']


class PollShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class UserAnswerSerializer(serializers.ModelSerializer):
    question = QuestionShortSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'text']


class UserPollSerializer(serializers.ModelSerializer):
    ids = []
    user_answers = UserAnswerSerializer(many=True)

    class Meta:
        model = UserPoll
        fields = ['user_id', 'poll', 'user_answers']

    def set_question_ids(self, ids: list):
        self.ids = ids

    def get_question_ids(self):
        return self.ids

    def create(self, validated_data):
        user_answers = validated_data.pop("user_answers")
        user_poll = UserPoll.objects.create(**validated_data)

        question_ids = self.get_question_ids()
        question_id_index = 0

        for user_answer in user_answers:
            question = Question.objects.get(id=question_ids[question_id_index])
            UserAnswer.objects.create(
                text=user_answer.get("text"),
                user_poll=user_poll,
                question=question
            )
            question_id_index += 1
        return user_poll

    def update(self, instance, validated_data):
        user_answers = validated_data.pop("user_answers")

        question_ids = self.get_question_ids()
        question_id_index = 0

        for user_answer in user_answers:
            user_answer_existing = UserAnswer.objects.get(
                user_poll=instance.id,
                question=question_ids[question_id_index]
            )
            user_answer_existing.text = user_answer.get("text")
            user_answer_existing.save()
            question_id_index += 1

        return instance
