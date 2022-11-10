import pytest

from taxi.models import Car, Driver, Manufacturer


@pytest.fixture
def manufacturers_data():
    data = [
        ("BMW", "Germany"),
        ("Toyota", "Japan"),
        ("Honda", "Japan"),
    ]

    for name, country in data:
        Manufacturer.objects.create(name=name, country=country)


@pytest.fixture
def drivers_data():
    data = [
        {
            "username": "user_1",
            "password": "zLjyFH7qd1icr33e",
            "first_name": "User",
            "last_name": "One",
            "license_number": "AAA12345",
        },
        {
            "username": "user_2",
            "password": "xFRKQuyqRa4pAs2t",
            "first_name": "User",
            "last_name": "Two",
            "license_number": "BBB23456",
        },
        {
            "username": "user_3",
            "password": "ilV5uG1y7UEkSowR",
            "first_name": "User",
            "last_name": "Three",
            "license_number": "CCC34567",
        },
    ]

    for user_data in data:
        Driver.objects.create_user(**user_data)


@pytest.fixture
def cars_data():
    data = [
        {"model": "x5", "manufacturer_id": 1, "driver_ids": [1]},
        {"model": "Corolla", "manufacturer_id": 2, "driver_ids": [1, 2, 3]},
    ]

    for car_data in data:
        car = Car.objects.create(
            model=car_data["model"],
            manufacturer_id=car_data["manufacturer_id"],
        )
        car.drivers.set(car_data["driver_ids"])


@pytest.fixture
def driver_client(client):
    driver = Driver.objects.create_user(
        username="client",
        password="zLjyFH7qd1icr33e",
        first_name="Client",
        last_name="Driver",
        license_number="CCC11111",
    )
    client.force_login(driver)

    return client
