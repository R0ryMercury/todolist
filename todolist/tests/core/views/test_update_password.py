import pytest

from rest_framework import status

UPDATE_PASS_URL = "/core/update_password"


@pytest.mark.django_db
def test_auth_required(client):
    response = client.get(
        UPDATE_PASS_URL,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
