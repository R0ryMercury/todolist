import pytest
from rest_framework import status

from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_auth_required(client, board):
    response = client.get("/goals/goal/{goal.id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
