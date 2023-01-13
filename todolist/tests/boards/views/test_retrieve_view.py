import pytest
from rest_framework import status

from goals.serializers import BoardSerializer


@pytest.mark.django_db
def test_auth_required(client, board):
    response = client.get(f"/goals/board/{board.pk}")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_retrieve_board(client, user, board, board_participant):
    client.force_login(user)
    response = client.get(f"/goals/board/{board.pk}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BoardSerializer(board).data
