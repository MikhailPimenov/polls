from django.db import models


class AnswerOption(models.Model):
    text = models.CharField(max_length=20, default=None)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        'Question',
        related_name='answer_options',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'answer_option'
        verbose_name_plural = 'answer_options'

    def __str__(self):
        return f'answer_option {self.text}'
