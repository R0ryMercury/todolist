import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User


@pytest.mark.django_db
def test_user_not_found(client, user: User):
    response = client.post(
        "/core/login",
        data={
            "username": user.username,
            "password": user.password,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "non_field_errors": ["username or password is incorrect"]
    }
