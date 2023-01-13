import pytest
from rest_framework import status

from goals.serializers import BoardSerializer


@pytest.mark.django_db
def test_auth_required(client, board, user, board_participant):
    response = client.get(f"/goals/board/{board.pk}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
