from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class TestPublicAccess(TestCase):
    MANUFACTURER_UPDATE_URL = None
    MANUFACTURER_DELETE_URL = None
    CAR_DETAIL_URL = None
    CAR_UPDATE_URL = None
    CAR_DELETE_URL = None
    DRIVER_DETAIL_URL = None
    DRIVER_UPDATE_URL = None
    DRIVER_DELETE_URL = None

    def setUp(self):
        self.client = Client()
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        driver = get_user_model().objects.create_user(
            username="Test Driver",
            password="test1234",
            first_name="Test First",
            last_name="Test Last"
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )
        self.MANUFACTURER_UPDATE_URL = reverse(
            "taxi:manufacturer-update", kwargs={"pk": manufacturer.pk}
        )
        self.MANUFACTURER_DELETE_URL = reverse(
            "taxi:manufacturer-delete", kwargs={"pk": manufacturer.pk}
        )
        self.CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": car.pk})
        self.CAR_UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": car.pk})
        self.CAR_DELETE_URL = reverse(
            "taxi:car-delete", kwargs={"pk": car.pk}
        )
        self.DRIVER_DETAIL_URL = reverse(
            "taxi:driver-detail", kwargs={"pk": driver.pk}
        )
        self.DRIVER_UPDATE_URL = reverse(
            "taxi:driver-update", kwargs={"pk": driver.pk}
        )
        self.DRIVER_DELETE_URL = reverse(
            "taxi:driver-delete", kwargs={"pk": driver.pk}
        )

    def test_login_required(self):
        urls = (
            MANUFACTURER_LIST_URL,
            MANUFACTURER_CREATE_URL,
            self.MANUFACTURER_UPDATE_URL,
            self.MANUFACTURER_DELETE_URL,
            CAR_LIST_URL,
            self.CAR_DETAIL_URL,
            CAR_CREATE_URL,
            self.CAR_UPDATE_URL,
            self.CAR_DELETE_URL,
            DRIVER_LIST_URL,
            self.DRIVER_DETAIL_URL,
            DRIVER_CREATE_URL,
            self.DRIVER_UPDATE_URL,
            self.DRIVER_DELETE_URL,
        )
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class TestPrivateAccess(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test Driver",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Test Manufacturer1",
            country="Test Country1"
        )
        Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="Test Country2"
        )
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class TestPrivateDriver(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test Driver",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "us3r12t@st@new",
            "password2": "us3r12t@st@new",
            "license_number": "AAA55555",
            "first_name": "Test First",
            "last_name": "Test Last",
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(
            new_driver.first_name, form_data["first_name"]
        )
        self.assertEqual(
            new_driver.last_name, form_data["last_name"]
        )
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )
