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
    def are_question_ids_valid(question_ids: list, poll_id) -> bool:
        for question_id in question_ids:
            if not (Question.objects.filter(pk=question_id).exists()
                    and Question.objects.get(pk=question_id).poll.id == int(poll_id)):
                return False
        return True

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
    def get_body_and_add_parameters(request, user_id, poll_id):
        user_poll = request.data
        user_poll["user_id"] = user_id
        user_poll["poll"] = poll_id
        return user_poll

    @staticmethod
    def get_question_ids_and_send_to_serializer(user_poll, serializer):
        question_ids = []
        for user_answer in user_poll.get("user_answers"):
            question_ids.append(user_answer["question_id"])
        serializer.set_question_ids(question_ids)
        return question_ids

    def modify_database_and_send_response(self, question_ids, user_id, poll_id, serializer, success_status,
                                          success_action_message):
        if not self.are_question_ids_valid(question_ids, poll_id):
            return Response({"error": f'poll={poll_id} does not have questions you listed'}, status=400)

        if not serializer.is_valid(raise_exception=True):
            return Response({"error": serializer.errors}, status=400)

        serializer.save()
        return Response(
            {"success": f'user_poll user_id={user_id} poll={poll_id} {success_action_message} successfully'},
            status=success_status)

    def create_new_user_poll(self, request, user_id, poll_id):
        user_poll = self.get_body_and_add_parameters(request, user_id, poll_id)

        serializer = UserPollSerializer(data=user_poll)

        question_ids = self.get_question_ids_and_send_to_serializer(user_poll, serializer)
        SUCCESS_STATUS_CONST = 201
        return self.modify_database_and_send_response(question_ids, user_id, poll_id, serializer, SUCCESS_STATUS_CONST,
                                                      'created')

    def update_existing_user_poll(self, request, user_id, poll_id):
        user_poll = self.get_body_and_add_parameters(request, user_id, poll_id)

        user_poll_saved = UserPoll.objects.get(user_id=user_id, poll=poll_id)
        serializer = UserPollSerializer(instance=user_poll_saved, data=user_poll, partial=True)

        question_ids = self.get_question_ids_and_send_to_serializer(user_poll, serializer)
        SUCCESS_STATUS_CONST = 200
        return self.modify_database_and_send_response(question_ids, user_id, poll_id, serializer, SUCCESS_STATUS_CONST,
                                                      'updated')

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
            return self.update_existing_user_poll(request, user_id, poll_id)
        except ValueError:
            return Response({"error": "invalid request parameters"}, status=400)
        except ObjectDoesNotExist:
            return self.create_new_user_poll(request, user_id, poll_id)

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
