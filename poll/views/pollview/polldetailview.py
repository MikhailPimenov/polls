from rest_framework import generics
from ...serializers import PollDetailSerializer
from ...models import Poll


class PollDetailView(generics.RetrieveAPIView):
    serializer_class = PollDetailSerializer
    queryset = Poll.objects.all()
