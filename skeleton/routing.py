from channels import route_class
from skeleton.consumers import EchoConsumer


channel_routing = [
    route_class(EchoConsumer, path=r"^/echo")
]
