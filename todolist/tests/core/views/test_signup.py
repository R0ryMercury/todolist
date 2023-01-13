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


@pytest.mark.django_db
def test_success_short(client, faker):
    assert not User.objects.count()
    password = faker.password()
    response = client.post(
        SIGNUP_URL,
        data={
            "username": faker.user_name(),
            "password": password,
            "password_repeat": password,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

    user = User.objects.last()
    assert response.json() == {
        "id": user.id,
        "username": user.username,
        "first_name": "",
        "last_name": "",
        "email": "",
    }
    assert user.password != password
    assert user.check_password(password)
