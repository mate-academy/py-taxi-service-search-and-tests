import pytest
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


# TODO: Ask if this is okay to use `parametrize()` like that.
@pytest.mark.parametrize(
    "model_instance, expected_output",
    [
        pytest.param(
            Manufacturer(name="Toyota", country="Japan"),
            "Toyota Japan",
            id="`str(Manufacturer)` should equal to "
            "`f'{Manufacturer.name} {Manufacturer.country}'`",
        ),
        pytest.param(
            Driver(
                username="user_1",
                password="7pJy2F0VGzg",
                first_name="User",
                last_name="One",
            ),
            "user_1 (User One)",
            id="`str(User)` should equal to "
            "`f'{User.username} ({User.first_name} {User.last_name})'`",
        ),
        pytest.param(
            Car(
                model="Corolla",
                manufacturer_id=2,
            ),
            "Corolla",
            id="`str(Car)` should equal to `Car.model`",
        ),
    ],
)
def test_str_methods(model_instance, expected_output):
    assert str(model_instance) == expected_output


@pytest.mark.parametrize(
    "driver_id",
    [
        pytest.param(1, id="should work for Driver with id 1"),
        pytest.param(3, id="should work for Driver with id other than 1"),
    ],
)
def test_driver_get_absolute_url(driver_id):
    driver = Driver(
        id=driver_id,
        username="user",
        password="7pJy2F0VGzg",
    )

    assert driver.get_absolute_url() == reverse(
        "taxi:driver-detail", kwargs={"pk": driver_id}
    )


@pytest.mark.django_db
def test_driver_creation():
    username = "user"
    password = "7pJy2F0VGzg"
    license_number = "AZR14125"

    driver = Driver.objects.create_user(
        username=username, password=password, license_number=license_number
    )

    assert (
        driver.username == username
    ), "Driver's username be equal to the passed value"

    assert driver.check_password(
        password
    ), "Driver's password should be equal to the passed value"

    assert (
        driver.license_number == license_number
    ), "Driver's license number should be equal to the passed value"
