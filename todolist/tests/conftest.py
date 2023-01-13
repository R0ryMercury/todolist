import pytest
from pytest_factoryboy import register

from tests.factories import (
    UserFactory,
    BoardFactory,
    BoardParticipantFactory,
    CategoryFactory,
    GoalFactory,
)


register(UserFactory)
register(BoardFactory)
register(BoardParticipantFactory)
register(CategoryFactory)
register(GoalFactory)
