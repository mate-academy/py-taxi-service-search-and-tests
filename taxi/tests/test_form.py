import pytest
from django.test import Client
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


@pytest.fixture
def authorize_user():
    user = Driver.objects.create_user(
        username="Test_name",
        password="Test_1234",
        license_number="ABC12345"
    )
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def db_objects():
    Manufacturer.objects.bulk_create(
        [
            Manufacturer(
                name=f"Test{i}_manufacturer",
                country="country"
            ) for i in range(15)
        ]
    )

    manufacturer = Manufacturer.objects.get(id=1)

    Car.objects.bulk_create(
        [
            Car(
                model=f"Test{i}_car",
                manufacturer=manufacturer
            ) for i in range(15)
        ]
    )
    Driver.objects.bulk_create(
        [
            Driver(
                username=f"Test{i}_user",
                password="Test_1234",
                license_number=f"AAA{i}") for i in range(10000, 10015)
        ]
    )


@pytest.mark.django_db
def test_correct_searching_manufacturer(authorize_user, db_objects):
    url = reverse("taxi:manufacturer-list") + "?name=2"
    res = authorize_user.get(url)

    assert res.status_code == 200
    assert "Test2_manufacturer" in res.content.decode()
    assert "Test12_manufacturer" in res.content.decode()
    assert "Test1_manufacturer" not in res.content.decode()


@pytest.mark.django_db
def test_correct_searching_car(authorize_user, db_objects):
    url = reverse("taxi:car-list") + "?model=2"
    res = authorize_user.get(url)

    assert res.status_code == 200
    assert "Test2_car" in res.content.decode()
    assert "Test12_car" in res.content.decode()
    assert "Test1_car" not in res.content.decode()


@pytest.mark.django_db
def test_correct_searching_driver(authorize_user, db_objects):
    url = reverse("taxi:driver-list") + "?username=2"
    res = authorize_user.get(url)

    assert res.status_code == 200
    assert "Test10002_user" in res.content.decode()
    assert "Test10012_user" in res.content.decode()
    assert "Test1001_user" not in res.content.decode()


@pytest.mark.django_db
def test_pagination_manufacturer(authorize_user, db_objects):
    url = reverse("taxi:manufacturer-list") + "?page=2"
    res = authorize_user.get(url)
    assert "next" in res.content.decode()
    assert "prev" in res.content.decode()


@pytest.mark.django_db
def test_pagination_car(authorize_user, db_objects):
    url = reverse("taxi:car-list") + "?page=2"
    res = authorize_user.get(url)
    assert "next" in res.content.decode()
    assert "prev" in res.content.decode()


@pytest.mark.django_db
def test_pagination_driver(authorize_user, db_objects):
    url = reverse("taxi:driver-list") + "?page=2"
    res = authorize_user.get(url)
    assert "next" in res.content.decode()
    assert "prev" in res.content.decode()
