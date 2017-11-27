from channels.test import ChannelTestCase, HttpClient


class TestEchoConsumer(ChannelTestCase):
    def test_channel(self):
        client = HttpClient()
        client.send_and_consume(channel=u"websocket.connect", path="/echo/")
        self.assertEqual("Hello, Anonymous", client.receive(json=False))
