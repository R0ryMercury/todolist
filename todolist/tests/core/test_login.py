import pytest
from rest_framework import status

from core.models import User

LOGIN_URL = "/core/login"


@pytest.mark.django_db
def test_user_not_found(client, user: User):
    response = client.post(
        LOGIN_URL,
        data={
            "username": user.username,
            "password": user.password,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "non_field_errors": ["username or password is incorrect"]
    }

@pytest.mark.django_db
def test_post_without_one_field(client, user: User):
    response = client.post(LOGIN_URL, data={"username": user.username})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"password": ["This field is required."]}

    response = client.post(LOGIN_URL, data={"password": user.password})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"username": ["This field is required."]}