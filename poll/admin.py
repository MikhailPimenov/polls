from django.contrib import admin
from nested_admin import nested

from .models import AnswerOption, Poll, Question, UserAnswer, UserPoll


class AnswerOptionAdminNested(nested.NestedStackedInline):
    model = AnswerOption
    extra = 2


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


class QuestionAdmin(nested.NestedModelAdmin):
    inlines = (AnswerOptionAdminNested,)


class UserAnswerAdminNested(nested.NestedStackedInline):
    model = UserAnswer
    extra = 0


class UserPollAdmin(nested.NestedModelAdmin):
    inlines = (UserAnswerAdminNested,)


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserPoll, UserPollAdmin)
