import pytest

from rest_framework import status

from core.models import User

SIGNUP_URL = "/core/signup"


@pytest.mark.django_db
def test_passwords_dont_match(client, faker):
    response = client.post(
        SIGNUP_URL,
        data={
            "username": faker.user_name(),
            "password": faker.password(),
            "password_repeat": faker.password(),
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"non_field_errors": ["passwords don't match"]}


