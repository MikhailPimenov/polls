from django.urls import path
from django.views.generic import TemplateView

from .views import PollDetailView, PollsAvailableListView, PollsListView, UserPollCreateView, UserPollsListView

urlpatterns = [
    path('api/poll/', PollsAvailableListView.as_view()),
    path('api/poll/all', PollsListView.as_view()),
    path('api/poll/detail/<int:pk>/', PollDetailView.as_view()),

    path('api/userpoll/<int:user_id>/', UserPollsListView.as_view()),
    path('api/userpoll/create/', UserPollCreateView.as_view()),

    path('swagger-ui/', TemplateView.as_view(
        template_name='poll/swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
