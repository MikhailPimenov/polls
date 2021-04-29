from django.http import Http404
from rest_framework import generics

from ..models import UserPoll
from ..serializers import UserPollCreateUpdateSerializer, UserPollDetailSerializer


class UserPollCreateView(generics.CreateAPIView):
    serializer_class = UserPollCreateUpdateSerializer


class UserPollsListView(generics.ListAPIView):
    serializer_class = UserPollDetailSerializer
    queryset = UserPoll.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = UserPoll.objects.filter(user_id=self.kwargs.get('user_id'))
        if not queryset.exists():  # or is it okay to return en empty queryset?
            raise Http404  # TODO: make this 404 exception more informative
        return queryset
