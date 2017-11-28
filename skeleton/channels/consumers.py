import logging

from channels.generic.websockets import WebsocketConsumer

logger = logging.getLogger(__name__)


class EchoConsumer(WebsocketConsumer):
    """
    A consumer that greets you (using your first name, if you are logged in)
    and afterwards simply echoes back what you say.
    """
    channel_session_user = True
    http_user = True

    def connect(self, message, **kwargs):
        """
        The websocket connection handler.

        :param message: A channels Message
        """
        logger.debug("A websocket connection was made by {}".format(
            message.user))
        # Accept the connection
        message.reply_channel.send({"accept": True})

        name = "" if message.user.is_anonymous else \
             message.user.first_name or message.user.username
        self.send(text="Hello, {}".format(name))

    def disconnect(self, message, **kwargs):
        """
        The websocket disconnection handler.

        :param message: A channels Message
        """
        logger.debug("{} disconnected a websocket".format(message.user))

    def receive(self, text=None, bytes=None, **kwargs):
        """
        This function simply echoes back a message received.
        """
        logger.debug("A websocket message was received from {}".format(
            self.message.user))
        logger.info("Got message: {}".format(text))
        self.send(text=text)
