from channels import route_class

from skeleton.channels.consumers import EchoConsumer


channel_routing = [
    route_class(EchoConsumer, path=r"^/ws/echo")
]
