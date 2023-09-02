from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})


class PublicDriverListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test1",
            password="password123",
            license_number="ABC00001"
        )
        get_user_model().objects.create_user(
            username="driver",
            password="password123",
            license_number="ABC00002"
        )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test3",
            password="password123",
            license_number="ABC00003"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_username(self):
        search_param = "driver"
        search_url = DRIVER_LIST_URL + "?username=" + search_param

        response = self.client.get(search_url)
        drivers = get_user_model().objects.filter(
            username__icontains=search_param
        )

        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )


class PublicDriverDetailTests(TestCase):
    def test_login_required(self):
        get_user_model().objects.create_user(
            username="test1",
            password="password123",
            license_number="ABC00001"
        )

        response = self.client.get(DRIVER_DETAIL_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverDetailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="driver",
            password="password123",
            license_number="ABC00001"
        )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        driver_detail = get_user_model().objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], driver_detail)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class PublicDriverCreateTests(TestCase):
    def test_public_login_required(self):
        response = self.client.get(reverse("taxi:driver-create"))

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverCreateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_create_driver_access(self):
        response = self.client.get(reverse("taxi:driver-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_create_driver(self):
        form_data = {
            "username": "tester",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first",
            "last_name": "last",
            "license_number": "ABC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PublicDriverUpdateTests(TestCase):
    def test_public_login_required(self):
        get_user_model().objects.create_user(
            username="test",
            password="password12345",
            license_number="ABC12345"
        )
        response = self.client.get(
            reverse("taxi:driver-update", kwargs={"pk": 1})
        )

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverUpdateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="driver",
            password="password123",
            license_number="ABC00001"
        )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_update_driver_access(self):
        response = self.client.get(
            reverse("taxi:driver-update", kwargs={"pk": 1})
        )
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], driver)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_update_driver(self):
        form_data = {"license_number": "CHG12345"}
        self.client.post(
            path=reverse("taxi:driver-update", kwargs={"pk": 1}),
            data=form_data
        )
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.license_number, form_data["license_number"])


class PublicDriverDeleteTests(TestCase):
    def test_public_login_required(self):
        get_user_model().objects.create_user(
            username="test",
            password="password12345",
            license_number="ABC12345"
        )
        response = self.client.get(
            reverse("taxi:driver-delete", kwargs={"pk": 1})
        )

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverDeleteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="driver",
            password="password123",
            license_number="ABC00001"
        )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_delete_driver(self):
        response = self.client.get(
            reverse("taxi:driver-delete", kwargs={"pk": 1})
        )
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], driver)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")
