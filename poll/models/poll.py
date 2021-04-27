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
