from django.db import models


class UserPoll(models.Model):
    user_id = models.IntegerField(default=0, null=False, blank=False)
    poll = models.ForeignKey('Poll', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'user_poll'
        verbose_name_plural = 'user_polls'

    def __str__(self):
        return f'user_poll {self.id} user: {self.user_id} poll: {self.poll.id}'
