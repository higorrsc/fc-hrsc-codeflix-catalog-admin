from src.core._shared.application.handler import AbstractHandler
from src.core._shared.events.event_dispatcher import EventDispatcher
from src.core.video.application.events.integration_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)


class PublishAudioVideoMediaUpdatedHandler(AbstractHandler):
    """
    Handler for the AudioVideoMediaUpdatedIntegrationEvent.
    """

    def __init__(self, event_dispatcher: EventDispatcher) -> None:
        """
        Constructor method.

        :param event_dispatcher: The event dispatcher to use when publishing the event.
        :type event_dispatcher: EventDispatcher
        """

        self.event_dispatcher = event_dispatcher

    def handle(self, event: AudioVideoMediaUpdatedIntegrationEvent) -> None:
        """
        Handle the AudioVideoMediaUpdatedIntegrationEvent.

        This method publishes the given event by printing it and dispatching it
        through the assigned event dispatcher.

        Args:
            event (AudioVideoMediaUpdatedIntegrationEvent): The event to be published.
        """

        self.event_dispatcher.dispatch(event)
        print(f"Publishing event: {event}")
