from django.db import models


class Question(models.Model):
    text = models.TextField(max_length=200)
    poll = models.ForeignKey(
        'Poll',
        related_name='questions',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

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
