import datetime
from rest_framework import generics

from ..models import Poll
from ..serializers import PollDetailSerializer, PollsListSerializer


class PollsAvailableListView(generics.ListAPIView):
    serializer_class = PollsListSerializer
    queryset = Poll.objects.filter(
        start_date__lte=datetime.datetime.now(),
        end_date__gte=datetime.datetime.now(),
    )


class PollsListView(generics.ListAPIView):
    serializer_class = PollsListSerializer
    queryset = Poll.objects.all()


class PollDetailView(generics.RetrieveAPIView):
    serializer_class = PollDetailSerializer
    queryset = Poll.objects.all()
