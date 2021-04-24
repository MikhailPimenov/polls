from abc import ABC, abstractmethod
from rest_framework.response import Response
from .serializers import UserPollSerializer
from .models import UserPoll, Question


class AbstractClass(ABC):
    def template_method(self, request, user_id, poll_id):
        user_poll = self.get_body_and_add_parameters(
            request=request,
            user_id=user_id,
            poll_id=poll_id
        )

        serializer, SUCCESS_STATUS_CONST, SUCCESS_ACTION_MESSAGE_CONST = \
            self.required_operations(user_poll=user_poll)

        question_ids = self.get_question_ids_and_send_to_serializer(
            user_poll=user_poll,
            serializer=serializer
        )

        return self.modify_database_and_send_response(
            question_ids=question_ids,
            user_id=user_id,
            poll_id=poll_id,
            serializer=serializer,
            success_status=SUCCESS_STATUS_CONST,
            success_action_message=SUCCESS_ACTION_MESSAGE_CONST
        )

    @abstractmethod
    def required_operations(self, user_poll) -> tuple:
        pass

    @staticmethod
    def are_question_ids_valid(question_ids: list, poll_id) -> bool:
        for question_id in question_ids:
            if not (Question.objects.filter(pk=question_id).exists()
                    and Question.objects.get(pk=question_id).poll.id == int(poll_id)):
                return False
        return True

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


class CreateUserPoll(AbstractClass):
    def required_operations(self, user_poll) -> tuple:
        serializer = UserPollSerializer(data=user_poll)
        SUCCESS_STATUS_CONST = 201
        SUCCESS_ACTION_MESSAGE_CONST = "created"
        return serializer, SUCCESS_STATUS_CONST, SUCCESS_ACTION_MESSAGE_CONST


class UpdateUserPoll(AbstractClass):
    def required_operations(self, user_poll) -> tuple:
        user_poll_saved = UserPoll.objects.get(user_id=user_poll["user_id"], poll=user_poll["poll"])
        serializer = UserPollSerializer(instance=user_poll_saved, data=user_poll, partial=True)
        SUCCESS_STATUS_CONST = 200
        SUCCESS_ACTION_MESSAGE_CONST = "updated"
        return serializer, SUCCESS_STATUS_CONST, SUCCESS_ACTION_MESSAGE_CONST
