from rest_framework import generics
from ...serializers import UserPollCreateUpdateSerializer


class UserPollCreateView(generics.CreateAPIView):
    serializer_class = UserPollCreateUpdateSerializer
