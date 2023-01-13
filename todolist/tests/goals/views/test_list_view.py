import pytest
from rest_framework import status


GOAL_URL = "/goals/goal/list"


@pytest.mark.django_db
def test_no_goals(client, user):
    client.force_login(user)
    response = client.get(GOAL_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
