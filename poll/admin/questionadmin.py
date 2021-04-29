from django.contrib import admin
from nested_admin import nested

from ..models import Question
from .answeroptionadmin import AnswerOptionAdminNested


class QuestionAdmin(nested.NestedModelAdmin):
    inlines = (AnswerOptionAdminNested,)


admin.site.register(Question, QuestionAdmin)
