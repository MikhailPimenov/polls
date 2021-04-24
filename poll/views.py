import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from .serializers import PollSerializer, UserPollSerializer, PollShortSerializer
from .models import Poll, UserPoll, Question
from rest_framework.generics import GenericAPIView
from drf_yasg2.utils import swagger_auto_schema
from .swagger import user_poll_put_parameters_for_documentation, \
    poll_get_parameters_for_documentation, user_poll_delete_parameters_for_documentation, \
    user_poll_get_parameters_for_documentation

from .create_update_user_poll import AbstractClass, CreateUserPoll, UpdateUserPoll


class PollAPIView(GenericAPIView):
    serializer_class = PollSerializer

    @staticmethod
    def get_queryset():
        return Poll.objects.all()

    @staticmethod
    def get_poll_with_id(poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            serializer = PollSerializer(poll)
            return Response(serializer.data, status=200)
        except ValueError:
            return Response({"error": "invalid request parameters"}, status=400)
        except ObjectDoesNotExist:
            return Response({"error": f'poll with id={poll_id} does not exist'}, status=404)

    @staticmethod
    def get_available_only_polls():
        polls = Poll.objects.filter(
            start_date__lte=datetime.datetime.now(),
            end_date__gte=datetime.datetime.now()
        )
        serializer = PollShortSerializer(polls, many=True)
        return Response(serializer.data, status=200)

    def get_all_polls(self):
        polls = self.get_queryset()
        serializer = PollShortSerializer(polls, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(**poll_get_parameters_for_documentation.get_parameters())
    def get(self, request):
        """Get all/all available/the exact(extended) poll(s)"""
        if "poll_id" in request.query_params:
            poll_id = request.query_params["poll_id"]
            return self.get_poll_with_id(poll_id)

        if "available_only" in request.query_params \
                and str(request.query_params["available_only"]).lower() == 'true':
            return self.get_available_only_polls()

        return self.get_all_polls()


class UserPollsAPIView(GenericAPIView):
    serializer_class = UserPollSerializer

    @staticmethod
    def get_query_set():
        return UserPoll.objects.all()

    def get_all_user_polls(self):
        user_polls = self.get_query_set()
        serializer = UserPollSerializer(user_polls, many=True)
        return Response(serializer.data, status=200)

    @staticmethod
    def get_user_polls_with_user_id(user_id):
        try:
            user_polls = UserPoll.objects.filter(user_id=user_id)
            if not user_polls.exists():
                return Response({"error": f'user_polls user_id={user_id} do not exist'}, status=404)

            serializer = UserPollSerializer(user_polls, many=True)
            return Response(serializer.data, status=200)
        except ValueError:
            return Response({"error": "invalid request parameters"}, status=400)

    @swagger_auto_schema(**user_poll_get_parameters_for_documentation.get_parameters())
    def get(self, request):
        """Get all user_polls / all user_polls with user_id"""
        if "user_id" not in request.query_params:
            return self.get_all_user_polls()

        user_id = int(request.query_params["user_id"])
        return self.get_user_polls_with_user_id(user_id)

    # def create_new_user_poll(self, request, user_id, poll_id):
    #     user_poll = self.get_body_and_add_parameters(request, user_id, poll_id)
    #
    #     serializer = UserPollSerializer(data=user_poll)
    #
    #     question_ids = self.get_question_ids_and_send_to_serializer(user_poll, serializer)
    #     SUCCESS_STATUS_CONST = 201
    #     return self.modify_database_and_send_response(question_ids, user_id, poll_id, serializer, SUCCESS_STATUS_CONST,
    #                                                   'created')
    #
    # def update_existing_user_poll(self, request, user_id, poll_id):
    #     user_poll = self.get_body_and_add_parameters(request, user_id, poll_id)
    #
    #     user_poll_saved = UserPoll.objects.get(user_id=user_id, poll=poll_id)
    #     serializer = UserPollSerializer(instance=user_poll_saved, data=user_poll, partial=True)
    #
    #     question_ids = self.get_question_ids_and_send_to_serializer(user_poll, serializer)
    #     SUCCESS_STATUS_CONST = 200
    #     return self.modify_database_and_send_response(question_ids, user_id, poll_id, serializer, SUCCESS_STATUS_CONST,
    #                                                   'updated')

    @staticmethod
    def create_or_update(abstract_class: AbstractClass, request, user_id, poll_id):
        return abstract_class.template_method(request, user_id, poll_id)

    @swagger_auto_schema(**user_poll_put_parameters_for_documentation.get_parameters())
    def put(self, request):
        """Creates new or updates existing user_poll"""
        if "user_id" not in request.query_params or "poll_id" not in request.query_params:
            return Response({"error": "request parameters do not contain 'user_id' or/and 'poll_id'"},
                            status=400)

        user_id = request.query_params["user_id"]
        poll_id = request.query_params["poll_id"]

        if not Poll.objects.filter(id=poll_id).exists():
            return Response({"error": f'poll with id={poll_id} does not exist'}, status=404)

        try:
            return self.create_or_update(UpdateUserPoll(), request, user_id, poll_id)
        except ValueError:
            return Response({"error": "invalid request parameters"}, status=400)
        except ObjectDoesNotExist:
            return self.create_or_update(CreateUserPoll(), request, user_id, poll_id)

    @staticmethod
    @swagger_auto_schema(**user_poll_delete_parameters_for_documentation.get_parameters())
    def delete(request):
        """Delete user_poll with user_id and poll_id"""
        if "user_id" not in request.query_params or "poll_id" not in request.query_params:
            return Response({"error": "request parameters do not contain 'user_id' or/and 'poll_id'"},
                            status=400)

        user_id = int(request.query_params["user_id"])
        poll_id = int(request.query_params["poll_id"])

        try:
            user_poll = UserPoll.objects.get(user_id=user_id, poll=poll_id)
        except ValueError:
            return Response({"error": "invalid request parameters"}, status=400)
        except ObjectDoesNotExist:
            return Response({"message": f'user_poll user_id={user_id} poll={poll_id} was not found'},
                            status=404)
        user_poll.delete()
        return Response({"success": f'user_poll user_id={user_id} poll={poll_id} was deleted successfully'},
                        status=200)


class PollAPIView(GenericAPIView):
    serializer_class = PollSerializer

    @staticmethod
    def get_queryset():
        return Poll.objects.all()

    @staticmethod
    def get_poll_with_id(poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            serializer = PollSerializer(poll)
            return Response(serializer.data, status=200)
        except ValueError:
            return Response({"error": "invalid request parameters"}, status=400)
        except ObjectDoesNotExist:
            return Response({"error": f'poll with id={poll_id} does not exist'}, status=404)

    @staticmethod
    def get_available_only_polls():
        polls = Poll.objects.filter(
            start_date__lte=datetime.datetime.now(),
            end_date__gte=datetime.datetime.now()
        )
        serializer = PollShortSerializer(polls, many=True)
        return Response(serializer.data, status=200)

    def get_all_polls(self):
        polls = self.get_queryset()
        serializer = PollShortSerializer(polls, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(**poll_get_parameters_for_documentation.get_parameters())
    def get(self, request):
        """Get all/all available/the exact(extended) poll(s)"""
        if "poll_id" in request.query_params:
            poll_id = request.query_params["poll_id"]
            return self.get_poll_with_id(poll_id)

        if "available_only" in request.query_params \
                and str(request.query_params["available_only"]).lower() == 'true':
            return self.get_available_only_polls()

        return self.get_all_polls()
