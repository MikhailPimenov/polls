from django.contrib import admin
from .models import Poll, Question, AnswerOption, UserPoll, UserAnswer
import nested_admin


class AnswerAdminNested(nested_admin.NestedStackedInline):
    model = AnswerOption
    extra = 2


class QuestionAdminNested(nested_admin.NestedStackedInline):
    model = Question
    inlines = (AnswerAdminNested,)


class PollAdmin(nested_admin.NestedModelAdmin):
    inlines = (QuestionAdminNested,)
    extra = 2

    def get_readonly_fields(self, request, objeect=None):
        if objeect:
            return self.readonly_fields + ('start_date',)
        return self.readonly_fields


class QuestionAdmin(admin.ModelAdmin):
    model = Question


class UserAnswerAdmin(admin.StackedInline):
    model = UserAnswer
    extra = 0


class UserPollAdmin(admin.ModelAdmin):
    inlines = (UserAnswerAdmin,)


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserPoll, UserPollAdmin)
