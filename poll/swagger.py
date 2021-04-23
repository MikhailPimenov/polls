from drf_yasg2 import openapi
from drf_yasg2.utils import status

from .serializers import PollSerializer, UserPollSerializer

answer_option_short = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'text': openapi.Schema(
            type=openapi.TYPE_STRING,
            example="text of the answer option"
        )
    },

)

question = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            example=1
        ),
        'text': openapi.Schema(
            type=openapi.TYPE_STRING,
            example='text of the question'
        ),
        'kind': openapi.Schema(
            type=openapi.TYPE_STRING,
            example='MA'
        ),
        'answer_options': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=answer_option_short
        )

    }
)

poll_id = openapi.Parameter(
    "poll_id",
    in_=openapi.IN_QUERY,
    description="Id of poll you want to know about",
    type=openapi.TYPE_INTEGER
)


class PollGetParametersForDocumentation:
    available_only = openapi.Parameter(
        "available_only",
        in_=openapi.IN_QUERY,
        description="Set it 'true' if you need only available polls",
        type=openapi.TYPE_BOOLEAN
    )

    response_400 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="invalid request parameters"
            )
        },
        description="Request parameters are null or inappropriate type"
    )

    response_404 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="poll with id=0 does not exist"
            )
        },
        description="There is no poll with that id"
    )

    def __init__(self):
        self.manual_parameters = [poll_id, self.available_only]

        self.responses = {
            status.HTTP_200_OK: PollSerializer,
            status.HTTP_400_BAD_REQUEST: self.response_400,
            status.HTTP_404_NOT_FOUND: self.response_404
        }

    def get_parameters(self) -> dict:
        return {
            "manual_parameters": self.manual_parameters,
            "responses": self.responses
        }


poll_get_parameters_for_documentation = PollGetParametersForDocumentation()

user_id_required = openapi.Parameter(
    "user_id",
    in_=openapi.IN_QUERY,
    required=True,
    description="Id of user you want to know about",
    type=openapi.TYPE_INTEGER
)
poll_id_required = openapi.Parameter(
    "poll_id",
    in_=openapi.IN_QUERY,
    required=True,
    description="Id of poll you want to know about",
    type=openapi.TYPE_INTEGER
)


class UserPollPutParametersForDocumentation:
    response_200 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="user_poll user_id=0 poll=1 updated successfully"
            )
        },
        description="Successful update of user_poll"
    )
    response_201 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="user_poll user_id=0 poll=1 created successfully"
            )
        },
        description="Successful creation of user_poll"
    )
    response_400 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="invalid request parameters"
            )
        },
        description="Bad request parameters"
    )
    response_404 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="poll with id=0 does not exist"
            )
        },
        description="Bad poll_id"
    )

    def __init__(self):
        self.manual_parameters = [user_id_required, poll_id_required]

        self.request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_answers': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'question_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'text': openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    ),
                    example=[
                        {'question_id': 1, 'text': 'user_answer 1'},
                        {'question_id': 2, 'text': 'user_answer 2'},
                    ]
                )
            }
        )

        self.responses = {
            status.HTTP_200_OK: self.response_200,
            status.HTTP_201_CREATED: self.response_201,
            status.HTTP_400_BAD_REQUEST: self.response_400,
            status.HTTP_404_NOT_FOUND: self.response_404,
        }

    def get_parameters(self) -> dict:
        return {
            "manual_parameters": self.manual_parameters,
            "request_body": self.request_body,
            "responses": self.responses
        }


class UserPollDeleteParametersForDocumentation:
    response_200 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="user_poll user_id=0 poll=0 was deleted successfully"
            )
        },
        description="Successful deletion of user_poll"
    )

    response_400 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="invalid request parameters"
            )
        },
        description="Bad request parameters"
    )

    response_404 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="user_poll user_id=0 poll_id=0 was not found"
            )
        },
        description="Bad poll_id and/or user_id"
    )

    def __init__(self):
        self.manual_parameters = [user_id, poll_id]

        self.responses = {
            status.HTTP_200_OK: self.response_200,
            status.HTTP_400_BAD_REQUEST: self.response_400,
            status.HTTP_404_NOT_FOUND: self.response_404
        }

    def get_parameters(self) -> dict:
        return {
            "manual_parameters": self.manual_parameters,
            "responses": self.responses
        }


user_id = openapi.Parameter(
    "user_id",
    in_=openapi.IN_QUERY,
    description="Id of user you want to know about",
    type=openapi.TYPE_INTEGER
)


class UserPollGetParametersForDocumentation:
    response_400 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="invalid request parameters"
            )
        },
        description="Request parameters are null or inappropriate type"
    )

    response_404 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="user_polls user_id=0 do not exist"
            )
        },
        description="There are no user_polls with that user_id"
    )

    def __init__(self):
        self.manual_parameters = [user_id]

        self.responses = {
            status.HTTP_200_OK: UserPollSerializer,
            status.HTTP_400_BAD_REQUEST: self.response_400,
            status.HTTP_404_NOT_FOUND: self.response_404
        }

    def get_parameters(self) -> dict:
        return {
            "manual_parameters": self.manual_parameters,
            "responses": self.responses
        }


user_poll_put_parameters_for_documentation = UserPollPutParametersForDocumentation()
user_poll_get_parameters_for_documentation = UserPollGetParametersForDocumentation()
user_poll_delete_parameters_for_documentation = UserPollDeleteParametersForDocumentation()

