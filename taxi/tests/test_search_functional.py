import pytest
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car

pytestmark = pytest.mark.django_db


@pytest.fixture
def logged_in_user(client):
    user = Driver.objects.create_user(
        username="test_user",
        password="password123",
    )
    client.force_login(user)
    return client


@pytest.fixture
def sample_data():
    toyota = Manufacturer.objects.create(
        name="Toyota"
    )
    ford = Manufacturer.objects.create(
        name="Ford"
    )

    driver1 = Driver.objects.create_user(
        username="john_doe",
        password="password",
        license_number="ABC12345",
    )
    driver2 = Driver.objects.create_user(
        username="jane_doe",
        password="password",
        license_number="AAA12345",
    )

    car1 = Car.objects.create(
        model="Camry",
        manufacturer=toyota,
    )
    car1.drivers.add(driver1)
    car2 = Car.objects.create(
        model="Focus",
        manufacturer=ford,
    )
    car2.drivers.add(driver2)


def test_driver_search_correct_count(logged_in_user, sample_data):
    response = logged_in_user.get(
        reverse("taxi:driver-list"),
        {"username": "john_doe"}
    )
    assert len(response.context["object_list"]) == 1


def test_driver_search_exact_username(logged_in_user, sample_data):
    response = logged_in_user.get(
        reverse("taxi:driver-list"),
        {"username": "john_doe"}
    )
    assert response.context["object_list"][0].username == "john_doe"


def test_driver_search_not_existing(logged_in_user, sample_data):
    response = logged_in_user.get(
        reverse("taxi:driver-list"),
        {"username": "not_existing_username"}
    )
    assert len(response.context["object_list"]) == 0


def test_manufacturer_search_correct_count(logged_in_user, sample_data):
    response = logged_in_user.get(
        reverse("taxi:manufacturer-list"),
        {"name": "Toyota"}
    )
    assert len(response.context["object_list"]) == 1


def test_manufacturer_search_exact_name(logged_in_user, sample_data):
    response = logged_in_user.get(
        reverse("taxi:manufacturer-list"),
        {"name": "Toyota"}
    )
    assert response.context["object_list"][0].name == "Toyota"


def test_manufacturer_search_not_existing(logged_in_user, sample_data):
    response = logged_in_user.get(
        reverse("taxi:manufacturer-list"),
        {"name": "not_existing_name"}
    )
    assert len(response.context["object_list"]) == 0


def test_car_search_correct_count(logged_in_user, sample_data):
    response = logged_in_user.get(
        reverse("taxi:car-list"),
        {"model": "Camry"}
    )
    assert len(response.context["object_list"]) == 1


def test_car_search_exact_model(logged_in_user, sample_data):
    response = logged_in_user.get(
        reverse("taxi:car-list"),
        {"model": "Camry"}
    )
    assert response.context["object_list"][0].model == "Camry"


def test_car_search_not_existing(logged_in_user, sample_data):
    response = logged_in_user.get(
        reverse("taxi:car-list"),
        {"model": "not_existing"}
    )
    assert len(response.context["object_list"]) == 0
