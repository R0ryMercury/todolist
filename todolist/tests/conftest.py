import pytest

from core.models import User


@pytest.fixture
@pytest.mark.django_db
def user(faker, django_user_model) -> User:
    user_data: dict[str, str] = {
        "username": faker.user_name(),
        "password": faker.password(),
    }
    if "email" in User.REQUIRED_FIELDS:
        user_data["email"] = faker.email()

    return django_user_model.objects.create_user(**user_data)
