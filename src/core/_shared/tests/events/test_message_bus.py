from unittest.mock import create_autospec

from src.core._shared.application.handler import AbstractHandler
from src.core._shared.events.event import Event
from src.core._shared.events.message_bus import MessageBus


class DummyEvent(Event):
    """
    Dummy event
    """


class TestMessageBus:
    """
    Test the message bus
    """

    def test_calls_correct_handler_with_event(self):
        """
        Tests that the handle method of the message bus calls the correct handler
        with the given event.
        """

        dummy_handler = create_autospec(AbstractHandler)
        message_bus = MessageBus()
        event = DummyEvent()

        message_bus.handlers[DummyEvent] = [dummy_handler]
        message_bus.handle([event])

        dummy_handler.handle.assert_called_once_with(event)
