import pytest
from rest_framework import status

PROFILE_URL = "/core/profile"


@pytest.mark.django_db
def test_auth_required(client):
    response = client.get(
        PROFILE_URL,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


