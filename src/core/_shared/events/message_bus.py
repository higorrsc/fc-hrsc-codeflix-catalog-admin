from typing import List, Type

from src.core._shared.application.handler import AbstractHandler
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.events.event import Event
from src.core._shared.infrastructure.events.rabbitmq_dispatcher import (
    RabbitMQDispatcher,
)
from src.core.video.application.events.handlers import (
    PublishAudioVideoMediaUpdatedHandler,
)
from src.core.video.application.events.integration_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)


class MessageBus(AbstractMessageBus):
    """
    Concrete implementation of a message bus.
    """

    def __init__(self) -> None:
        self.handlers: dict[Type[Event], List[AbstractHandler]] = {
            AudioVideoMediaUpdatedIntegrationEvent: [
                PublishAudioVideoMediaUpdatedHandler(
                    event_dispatcher=RabbitMQDispatcher(queue_name="videos.new")
                )
            ],
        }

    def handle(self, events: List[Event]) -> None:
        """
        Handle the given events.

        Args:
            events (List[Event]): The events to handle.
        """

        for event in events:
            handlers = self.handlers.get(type(event), [])
            for handler in handlers:
                try:
                    handler.handle(event)
                except Exception as e:
                    print(f"Error handling event {event}: {e}")
