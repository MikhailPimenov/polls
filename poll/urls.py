from django.urls import path
from django.views.generic import TemplateView

from .views import PollAPIView, UserPollsAPIView

urlpatterns = [
    path('api/poll', PollAPIView.as_view()),
    path('api/userpoll', UserPollsAPIView.as_view()),
    path('swagger-ui/', TemplateView.as_view(
        template_name='poll/swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
