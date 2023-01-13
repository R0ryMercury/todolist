import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User


@pytest.mark.django_db
def test_user_not_found(client, user: User):
    response = client.post(
        reverse("login"),
        data={
            "username": user.username,
            "password": user.password,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Incorrect authentication credentials."}

