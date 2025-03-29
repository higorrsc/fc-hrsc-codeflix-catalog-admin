from unittest.mock import create_autospec

from src.core._shared.domain.entity import AbstractEntity
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.events.event import Event


class DummyEvent(Event):
    """
    Dummy event
    """


class DummyEntity(AbstractEntity):
    """
    Dummy entity
    """

    def validate(self):
        """
        Validate the entity.

        This method should be implemented in the concrete subclasses to validate
        the entity's state. It should raise a ValueError if the entity is in an
        invalid state.

        Raises:
            ValueError: If the entity is in an invalid state.
        """


class TestDispatch:
    """
    Test the dispatch method
    """

    def test_dispatch(self):
        """
        Test the dispatch method.

        This test verifies that the dispatch method adds the given event to the
        entity's events list and calls the message bus's handle method with the
        events list.
        """

        mock_message_bus = create_autospec(AbstractMessageBus)
        entity = DummyEntity(message_bus=mock_message_bus)
        entity.dispatch(DummyEvent())
        assert entity.events == [DummyEvent()]
        mock_message_bus.handle.assert_called_once_with(entity.events)
