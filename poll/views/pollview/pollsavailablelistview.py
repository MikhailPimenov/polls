import datetime
from rest_framework import generics
from ...serializers import PollsListSerializer
from ...models import Poll


class PollsAvailableListView(generics.ListAPIView):
    serializer_class = PollsListSerializer
    queryset = Poll.objects.filter(
        start_date__lte=datetime.datetime.now(),
        end_date__gte=datetime.datetime.now(),
    )
