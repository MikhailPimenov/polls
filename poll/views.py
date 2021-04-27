import datetime
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Poll, Question, UserPoll
from .serializers import PollSerializer, PollShortSerializer, UserPollSerializer
from .swagger import (
    poll_get_parameters_for_documentation,
    user_poll_delete_parameters_for_documentation,
    user_poll_get_parameters_for_documentation,
    user_poll_put_parameters_for_documentation
)


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

    @staticmethod
    def get_serializer_for_creating(user_poll):
        serializer = UserPollSerializer(data=user_poll)
        return serializer

    @staticmethod
    def get_serializer_for_updating(user_poll):
        user_poll_saved = UserPoll.objects.get(
            user_id=user_poll["user_id"],
            poll=user_poll["poll"]
        )
        serializer = UserPollSerializer(
            instance=user_poll_saved,
            data=user_poll,
            partial=True
        )
        return serializer

    @staticmethod
    def get_response_data_for_creating():
        SUCCESS_STATUS_CONST = 201
        SUCCESS_ACTION_MESSAGE_CONST = "created"
        return SUCCESS_STATUS_CONST, SUCCESS_ACTION_MESSAGE_CONST

    @staticmethod
    def get_response_data_for_updating():
        SUCCESS_STATUS_CONST = 200
        SUCCESS_ACTION_MESSAGE_CONST = "updated"
        return SUCCESS_STATUS_CONST, SUCCESS_ACTION_MESSAGE_CONST

    @staticmethod
    def are_question_ids_valid(question_ids: list, poll_id) -> bool:
        for question_id in question_ids:
            if not Question.objects.filter(pk=question_id).exists() or \
                    not Question.objects.get(pk=question_id).poll.id == int(poll_id):
                return False
        return True

    def template_for_create_and_update(self, request, get_serializer, get_data_for_response):
        user_poll = request.data
        user_id = request.query_params["user_id"]
        poll_id = request.query_params["poll_id"]
        user_poll["user_id"] = user_id
        user_poll["poll"] = poll_id

        serializer = get_serializer(user_poll)

        question_ids = []
        for user_answer in user_poll.get("user_answers"):
            question_ids.append(user_answer["question_id"])
        serializer.set_question_ids(question_ids)

        if not self.are_question_ids_valid(question_ids, poll_id):
            return Response(
                {"error": f'poll={poll_id} does not have questions you listed'},
                status=400
            )

        if not serializer.is_valid(raise_exception=True):
            return Response({"error": serializer.errors}, status=400)

        serializer.save()

        SUCCESS_STATUS_CONST, SUCCESS_ACTION_MESSAGE_CONST = get_data_for_response()

        return Response(
            {"success": f'user_poll user_id={user_id} poll={poll_id} {SUCCESS_ACTION_MESSAGE_CONST} successfully'},
            status=SUCCESS_STATUS_CONST
        )

    @swagger_auto_schema(**user_poll_put_parameters_for_documentation.get_parameters())
    def put(self, request):
        """Creates new or updates existing user_poll"""
        if "user_id" not in request.query_params or "poll_id" not in request.query_params:
            return Response(
                {"error": "request parameters do not contain 'user_id' or/and 'poll_id'"},
                status=400
            )

        if not Poll.objects.filter(id=request.query_params["poll_id"]).exists():
            return Response(
                {"error": f'poll with id={request.query_params["poll_id"]} does not exist'},
                status=404
            )

        try:
            return self.template_for_create_and_update(
                request=request,
                get_serializer=self.get_serializer_for_updating,
                get_data_for_response=self.get_response_data_for_updating,
            )
        except ValueError:
            return Response({"error": "invalid request parameters"}, status=400)
        except ObjectDoesNotExist:
            return self.template_for_create_and_update(
                request=request,
                get_serializer=self.get_serializer_for_creating,
                get_data_for_response=self.get_response_data_for_creating,
            )

    @staticmethod
    @swagger_auto_schema(**user_poll_delete_parameters_for_documentation.get_parameters())
    def delete(request):
        """Delete user_poll with user_id and poll_id"""
        if "user_id" not in request.query_params or "poll_id" not in request.query_params:
            return Response(
                {"error": "request parameters do not contain 'user_id' or/and 'poll_id'"},
                status=400
            )

        user_id = int(request.query_params["user_id"])
        poll_id = int(request.query_params["poll_id"])

        try:
            user_poll = UserPoll.objects.get(user_id=user_id, poll=poll_id)
        except ValueError:
            return Response({"error": "invalid request parameters"}, status=400)
        except ObjectDoesNotExist:
            return Response(
                {"message": f'user_poll user_id={user_id} poll={poll_id} was not found'},
                status=404
            )
        user_poll.delete()
        return Response(
            {"success": f'user_poll user_id={user_id} poll={poll_id} was deleted successfully'},
            status=200
        )


