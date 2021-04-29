from django.contrib import admin
from nested_admin import nested

from ..models import Poll, Question
from .answeroptionadmin import AnswerOptionAdminNested


class QuestionAdminNested(nested.NestedStackedInline):
    model = Question
    inlines = (AnswerOptionAdminNested,)


class PollAdmin(nested.NestedModelAdmin):
    inlines = (QuestionAdminNested,)
    extra = 2

    def get_readonly_fields(self, request, objeect=None):
        if objeect:
            return self.readonly_fields + ('start_date',)
        return self.readonly_fields


admin.site.register(Poll, PollAdmin)
