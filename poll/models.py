from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=50, default='poll_name')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(max_length=200, default='poll_description')

    class Meta:
        verbose_name = 'poll'
        verbose_name_plural = 'polls'

    def __str__(self):
        return f'poll {self.id} {self.name} created at {self.start_date}'


class Question(models.Model):
    text = models.TextField(max_length=200)
    poll = models.ForeignKey(Poll, related_name='questions', null=True, blank=True, on_delete=models.CASCADE)

    TEXT_ANSWER = 'TA'
    SINGLE_ANSWER = 'SA'
    MULTIPLE_ANSWER = 'MA'

    KIND_CHOICES = [
        (TEXT_ANSWER, 'text answer'),
        (SINGLE_ANSWER, 'single answer'),
        (MULTIPLE_ANSWER, 'multiple answer'),
    ]

    kind = models.CharField(max_length=2, choices=KIND_CHOICES, default=TEXT_ANSWER)

    class Meta:
        verbose_name = 'question'
        verbose_name_plural = 'questions'

    def __str__(self):
        return f'question {self.id} ({self.kind}): {self.text}'


class AnswerOption(models.Model):
    text = models.CharField(max_length=20, default=None)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name='answer_options', null=True, blank=True,
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'answer_option'
        verbose_name_plural = 'answer_options'

    def __str__(self):
        return f'answer_option {self.text}'


class UserPoll(models.Model):
    user_id = models.IntegerField(default=0, null=False, blank=False)
    poll = models.ForeignKey(Poll, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'user_poll'
        verbose_name_plural = 'user_polls'

    def __str__(self):
        return f'user_poll {self.id} user: {self.user_id} poll: {self.poll.id}'


class UserAnswer(models.Model):
    user_poll = models.ForeignKey(UserPoll, related_name='user_answers', null=True, blank=True,
                                  on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(null=True, blank=True, max_length=20)

    class Meta:
        verbose_name = 'user_answer'
        verbose_name_plural = 'user_answers'

    def __str__(self):
        return f'user_answer {self.id} on question {self.question.id}'
