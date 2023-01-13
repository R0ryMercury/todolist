import pytest

from rest_framework import status

BOARD_CREATE_URL = "/goals/board/create"


@pytest.mark.django_db
def test_auth_required(client, board):
    response = client.post(BOARD_CREATE_URL, data={"title": board.title})
    assert response.status_code == status.HTTP_403_FORBIDDEN


