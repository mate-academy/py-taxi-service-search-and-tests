import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Tavria", country="Ukraine")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer_all = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_all),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    @override_settings(AUTH_PASSWORD_VALIDATORS=[])
    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "Password1",
            "password2": "Password1",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "license_number": "HHH12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, "new_first_name")
        self.assertEqual(new_user.last_name, "new_last_name")
        self.assertEqual(new_user.license_number, "HHH12345")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "search_term,expected_results",
    [
        pytest.param(
            "testdriver",
            ["testdriver1",
             "testdriver2"],
            id="partial_match"
        ),
        pytest.param(
            "",
            ["testdriver1", "testdriver2", "driver3"],
            id="empty_search"
        ),
        pytest.param("nonexistent", [], id="no_results"),
    ],
)
def test_driver_search(client, search_term, expected_results):
    user = get_user_model().objects.create_user(
        username="testuser", password="testpass"
    )
    client.force_login(user)

    _ = Driver.objects.create(
        username="testdriver1",
        password="testpass",
        license_number="AAA11111"
    )
    _ = Driver.objects.create(
        username="testdriver2",
        password="testpass",
        license_number="BBB22222"
    )
    _ = Driver.objects.create(
        username="driver3",
        password="testpass",
        license_number="CCC33333"
    )

    response = client.get(
        reverse("taxi:driver-list"),
        {"username": search_term}
    )
    assert response.status_code == 200

    response_content = response.content.decode()
    for driver_username in expected_results:
        assert driver_username in response_content
    for driver in Driver.objects.exclude(username__in=expected_results):
        assert driver.username not in response_content


@pytest.mark.django_db
@pytest.mark.parametrize(
    "search_term,expected_results",
    [
        pytest.param("ModelX", ["ModelX1", "ModelX2"], id="partial_match"),
        pytest.param(
            "",
            ["ModelX1", "ModelX2", "ModelY1"],
            id="empty_search"),
        pytest.param("nonexistent", [], id="no_results"),
    ],
)
def test_car_search(client, search_term, expected_results):
    user = get_user_model().objects.create_user(
        username="testuser", password="testpass"
    )
    client.force_login(user)

    manufacturer = Manufacturer.objects.create(name="TestManufacturer")

    _ = Car.objects.create(model="ModelX1", manufacturer=manufacturer)
    _ = Car.objects.create(model="ModelX2", manufacturer=manufacturer)
    _ = Car.objects.create(model="ModelY1", manufacturer=manufacturer)

    response = client.get(reverse("taxi:car-list"), {"model": search_term})
    assert response.status_code == 200

    response_content = response.content.decode()
    for car_model in expected_results:
        assert car_model in response_content
    for car in Car.objects.exclude(model__in=expected_results):
        assert car.model not in response_content


@pytest.mark.django_db
@pytest.mark.parametrize(
    "search_term,expected_results",
    [
        pytest.param(
            "TestManufacturer",
            ["TestManufacturer1", "TestManufacturer2"],
            id="partial_match",
        ),
        pytest.param(
            "",
            ["TestManufacturer1", "TestManufacturer2", "OtherManufacturer"],
            id="empty_search",
        ),
        pytest.param("nonexistent", [], id="no_results"),
    ],
)
def test_manufacturer_search(client, search_term, expected_results):
    user = get_user_model().objects.create_user(
        username="testuser", password="testpass"
    )
    client.force_login(user)

    _ = Manufacturer.objects.create(name="TestManufacturer1")
    _ = Manufacturer.objects.create(name="TestManufacturer2")
    _ = Manufacturer.objects.create(name="OtherManufacturer")

    response = client.get(
        reverse("taxi:manufacturer-list"),
        {"name": search_term}
    )
    assert response.status_code == 200

    response_content = response.content.decode()
    for manufacturer_name in expected_results:
        assert manufacturer_name in response_content
    for manufacturer in Manufacturer.objects.exclude(
            name__in=expected_results
    ):
        assert manufacturer.name not in response_content


class DriverIntegrationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="adminuser", password="adminpass123"
        )
        self.client.force_login(self.user)

    @override_settings(AUTH_PASSWORD_VALIDATORS=[])
    def test_create_driver_and_check_in_list(self):
        form_data = {
            "username": "new_driver",
            "password1": "A1b2C3d4E5",
            "password2": "A1b2C3d4E5",
            "first_name": "New",
            "last_name": "Driver",
            "license_number": "XYZ98765",
        }

        create_response = self.client.post(
            reverse("taxi:driver-create"), data=form_data
        )

        if create_response.status_code != 302:
            print(create_response.context["form"].errors)
        self.assertEqual(create_response.status_code, 302)

        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertIsNotNone(new_driver)
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )

        list_response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, new_driver.username)
