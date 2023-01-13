import pytest
from rest_framework import status

from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_auth_required(client):
    response = client.get("/goals/goal/{goal.id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_goal_retrieve(client, user, goal, board_participant):
    client.force_login(user)
    response = client.get(f"/goals/goal/{goal.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == GoalSerializer(goal).data
