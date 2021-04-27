from django.db import models


class UserAnswer(models.Model):
    user_poll = models.ForeignKey(
        'UserPoll',
        related_name='user_answers',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey('Question', null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(null=True, blank=True, max_length=20)

    class Meta:
        verbose_name = 'user_answer'
        verbose_name_plural = 'user_answers'

    def __str__(self):
        return f'user_answer {self.id} on question {self.question.id}'
