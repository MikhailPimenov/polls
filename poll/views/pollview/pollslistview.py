from rest_framework import generics
from ...serializers import PollsListSerializer
from ...models import Poll


class PollsListView(generics.ListAPIView):
    serializer_class = PollsListSerializer
    queryset = Poll.objects.all()
