from nested_admin import nested

from ..models import AnswerOption


class AnswerOptionAdminNested(nested.NestedStackedInline):
    model = AnswerOption
    extra = 2
