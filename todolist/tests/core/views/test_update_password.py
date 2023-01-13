import pytest

from rest_framework import status

UPDATE_PASS_URL = "/core/update_password"


@pytest.mark.django_db
def test_auth_required(client):
    response = client.get(
        UPDATE_PASS_URL,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_invalid_old_password(client, user, faker):
    client.force_login(user)
    response = client.patch(
        UPDATE_PASS_URL,
        data={
            "old_password": faker.password(),
            "new_password": faker.password(),
        },
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json() == {"old_password": ["field is incorrect"]}


@pytest.mark.django_db
def test_success(client, user, faker):
    old_password = faker.password()
    user.set_password(old_password)
    user.save(update_fields=("password",))

    new_password = faker.password()
    client.force_login(user)
    response = client.patch(
        UPDATE_PASS_URL,
        data={
            "old_password": old_password,
            "new_password": new_password,
        },
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert not response.json()
    user.refresh_from_db(fields=("password",))
    assert user.check_password(new_password)
