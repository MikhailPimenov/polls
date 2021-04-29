from django.contrib import admin
from nested_admin import nested

from ..models import UserAnswer, UserPoll


class UserAnswerAdminNested(nested.NestedStackedInline):
    model = UserAnswer
    extra = 0


class UserPollAdmin(nested.NestedModelAdmin):
    inlines = (UserAnswerAdminNested,)


admin.site.register(UserPoll, UserPollAdmin)
