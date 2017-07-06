from channels import Channel
from datetime import datetime
import time
import json
import logging
import pprint
import requests
from uuid import uuid4

from kopano import utils
from kopano.models import PortalUser
from kopano.user_channels import get_user_channel

from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

UUID = settings.KOPANO["feersum"]["channel"]


CHANNELS = {
    UUID: {
        'id': UUID,
        'type': 'feersum-0.9',
        'label': 'Kopano Application',

        # mo_url is for Junebug HTTP api
        'mo_url': 'http://pce.qa.praekelt.com/channel/message',

        # amqp_queue is for Vumi-style RabbitMQ api
        # 'amqp_queue':

        'metadata': {
            # This is to auto-attach to the Project Version, Optional.
            # Assignment can be overridden in FE Admin interface.
            # If invalid, then ignored.
            'aspect': 'another-uuid',

            # States that it supports pre-specified message_id (recommended)
            # Set to false if you want to force message_id to be generated
            # on your side. (Only relevant over Junebug HTTP api.)
            'message_id': True,

            # Callback URL so that FE can request user details
            # The recepient-id will be specified as the next path
            # e.g. GET http://my-server/channels/requested-id/userinfo/recepient-id
            'userinfo':
                'http://kopano.demo.praekelt.com/portal/v1/feersum/channels/{'
                '}/userinfo/'.format(UUID)
        }
    },
    "cobusc-kopano-test": {
        'id': "cobusc-kopano-test",
        'type': 'feersum-0.9',
        'label': 'Cobusc Kopano Application Test',

        # mo_url is for Junebug HTTP api
        'mo_url': 'http://pce.qa.praekelt.com/channel/message',

        # amqp_queue is for Vumi-style RabbitMQ api
        # 'amqp_queue':

        'metadata': {
            # This is to auto-attach to the Project Version, Optional.
            # Assignment can be overridden in FE Admin interface.
            # If invalid, then ignored.
            'aspect': 'cobusc-another-uuid',

            # States that it supports pre-specified message_id (recommended)
            # Set to false if you want to force message_id to be generated
            # on your side. (Only relevant over Junebug HTTP api.)
            'message_id': True,

            # Callback URL so that FE can request user details
            # The recepient-id will be specified as the next path
            # e.g. GET http://my-server/channels/requested-id/userinfo/recepient-id
            'userinfo':
                'http://127.0.0.1:6666/portal/v1/feersum/channels/cobusc'
                '-kopano-test/userinfo/'
        }
    }
}

CHANNEL = CHANNELS[settings.KOPANO["feersum"]["channel"]]
FEERSUM_TIMEOUT = settings.KOPANO["feersum"]["timeout"]

# JSONSchema to validate callbacks
CALLBACK_SCHEMA = {
    "type": "object",
    "properties": {
        "to": {"type": "string"},
        "from": {"type": ["string", "null"]},
        "reply_to": {"type": "string"},
        "content": {"type": ["string", "null"]},
        "event_url": {"type": "string"},
        "priority": {"type": "string"},
        "channel_data": {"type": "object"},
    },
    "required": ["content"],
    "additionalProperties": False,
}

logger = logging.getLogger(__name__)


# # This function was hacked together based on the code here:
# # https://github.com/praekelt/webchat/blob/develop/webchat/views/chats.py
# def send_message(from_address, content="", meta=None, session_event="continue"):
#     # type: (dict, str, str, dict, str) -> None
#     """
#     Send a message to the Feersum Engine
#     :param from_address:
#     :param content:
#     :param meta:
#     :param session_event:
#     :return:
#     """
#     meta = meta or {}
#     meta["postback"] = FEERSUM_CALLBACK_URL
#
#     try:
#         data = json.dumps({
#             "channel_data": {
#                 "session_event": session_event,
#             },
#             "from": from_address,
#             "channel_id": FEERSUM_CHANNEL_ID,
#             "timestamp": str(datetime.utcnow()),
#             "content": content,
#             "to": FEERSUM_CHANNEL_ID,
#             "reply_to": None,
#             "message_id": str(uuid4())
#         })
#         pprint(data)
#         response = requests.post(FEERSUM_MO_URL, data=data)
#         if response.status_code != 200:
#             logger.error("Unexpected HTTP response code: {}".format(
#                 response.status_code))
#     except Exception as e:
#         logger.error(e)
#
#
# # This function was hacked together based on the code here:
# # https://github.com/praekelt/webchat/blob/develop/webchat/views/channels.py
# @require_http_methods(["POST"])
# def receive_message(request, channel_id):
#     # type: (Request) -> JsonResponse | HttpResponseBadRequest
#     """
#     Handles messages from the Feersum Engine to a connected chat user
#     :param request:
#     :param channel_id: The channel id provided by Feersum
#     :return: JsonResponse
#     """
#     if channel_id != FEERSUM_CHANNEL_ID:
#         return HttpResponseBadRequest("Unknown channel")
#
#     data = request["data"]
#     print("From Feersum:")
#     pprint(data)
#
#     # Forward channel_data to websocket
#     channel = Channel(data["to"])
#     channel.send({"text": json.dumps(data["channel_data"])})
#
#     return JsonResponse({
#         "code": "OK",
#         "status": 200,
#         "result": {
#             "content": "",
#             "message_id": str(uuid4()),
#             "timestamp": str(datetime.utcnow()),
#             "channel_id": FEERSUM_CHANNEL_ID
#         },
#         "description": "message sent"
#     })


@require_http_methods(["GET"])
def list_channels(request):
    return JsonResponse({
        "status": 200,
        "code": "OK",
        "description": "channels listed",
        "result": [CHANNEL["id"]]
    })


@require_http_methods(["GET"])
def get_channel(request, channel_id):
    if channel_id == CHANNEL["id"]:
        return JsonResponse({
            "status": 200,
            "code": "OK",
            "description": "channel found",
            "result": CHANNEL
        })

    return JsonResponse({
        "status": 404,
        "code": "Not Found",
    })


@csrf_exempt
@require_http_methods(["POST"])
def receive_message(request, channel_id):
    timestamp = str(datetime.utcnow())
    data = json.loads(request.body)
    pprint.pprint(data)
    message_id = data.get("message_id", str(uuid4()))
    # Forward channel_data to websocket
    reply_channel_id = utils.get_reply_channel(data["to"])
    try:
        channel = Channel(reply_channel_id)
        channel.send({"text": json.dumps(data["channel_data"])})
    except Exception as e:
        logger.error("Could not send message to websocket: {}".format(e))

    return JsonResponse({
        "code": "OK",
        "status": 200,
        "result": {
            "message_id": message_id,
            "timestamp": timestamp,
            "channel_id": CHANNEL["id"]
        },
        "description": "message sent"
    })


def send_message_http(_from, text="", postback=None, event="resume"):
    # type: (str, str, Dict|None) -> bool
    result = False
    try:
        data = {
            "from": _from,
            "channel_id": CHANNEL["id"],
            "timestamp": str(datetime.utcnow()),
            "content": text,
            "channel_data": {
                "session_event": event,
                #                **FEERSUM_META
            },
            "to": CHANNEL["id"],
            "message_id": str(uuid4())
        }
        if postback:
            data["channel_data"]["postback"] = postback

        pprint.pprint(data)
        response = requests.post(  # type: ignore
            CHANNEL["mo_url"],
            json=data
        )
        # pprint.pprint(result)
        pprint.pprint(response.status_code)
        # pprint.pprint(result.headers)
        # pprint.pprint(result.content)
        # pprint.pprint(result.text)
        result = response.status_code == 200
    except Exception as e:
        logger.error(e)
        pass

    return result


def get_message(cid, message_id, timestamp, _to, _from, session_event, text, meta):
    print(json.dumps({
        "cid": cid,
        "message_id": message_id,
        "timestamp": timestamp,
        "to": _to,
        "from": _from,
        "session_event": session_event,
        "text": text,
        "meta": meta
    }, indent=4, sort_keys=True))


def hello(request):
    user = "test"+str(time.time())
    response = requests.post(  # type: ignore
        CHANNEL["mo_url"],
        json={
            "from": user,
            "channel_id": CHANNEL["id"],
            "timestamp": str(datetime.utcnow()),
            "content": "ping",
            "channel_data": {
                "session_event": "resume",
#                **FEERSUM_META
            },
            "to": CHANNEL["id"],
            "message_id": str(uuid4())
        }
    )
    pprint.pprint(response)
    pprint.pprint(response.text)
    pprint.pprint(response.history)
    return JsonResponse({}, safe=False)


@require_http_methods(["GET"])
def get_user_info(request, channel_id, recipient_id):
    """
    Requests userinfo for specified channel:recepient combination.

    :param request:
    :param channel_id:
    :param recipient_id:
    :return:
    """
    if recipient_id.startswith(utils.KOPANO_USER_PREFIX):
        user = utils.get_user_from_address(recipient_id)
        return JsonResponse({
            "code": "OK",
            "status": 200,
            "result": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "extra": {
                    "policy_holder_id": user.policy_holder_id
                }
            }
        })
    elif recipient_id.startswith("daphne.response."):
        # This is a hack for now to "mock" users
        username = "test"+str(time.time())
        return JsonResponse({
            "code": "OK",
            "status": 200,
            "result": {
                "first_name": username + "_first_name",
                "last_name": username + "_last_name",
                "username": username,
                "email": username + "@example.com",
                "extra": {
                }
            }
        })
