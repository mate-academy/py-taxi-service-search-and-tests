from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


PK = "1"

DRIVER_LIST = reverse("taxi:driver-list")
DRIVER_CREATE = reverse("taxi:driver-create")
DRIVER_DETAIL = reverse("taxi:driver-detail", args=[PK])
DRIVER_LICENSE_UPDATE = reverse("taxi:driver-update", args=[PK])
DRIVER_DELETE = reverse("taxi:driver-delete", args=[PK])

TOGGLE_CAR_ASSIGN = reverse("taxi:toggle-car-assign", args=[PK])


class PublicDriverTests(TestCase):
    def setUp(self) -> None:

        get_user_model().objects.create_user(
            username="test",
            password="test123456"
        )

    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_LIST)

        self.assertNotEquals(response.status_code, 200)

    def test_driver_create_login_required(self):
        response = self.client.get(DRIVER_CREATE)

        self.assertNotEquals(response.status_code, 200)

    def test_driver_detail_login_required(self):
        response = self.client.get(DRIVER_DETAIL)

        self.assertNotEquals(response.status_code, 200)

    def test_driver_update_login_required(self):
        response = self.client.get(DRIVER_LICENSE_UPDATE)

        self.assertNotEquals(response.status_code, 200)

    def test_driver_delete_login_required(self):
        response = self.client.get(DRIVER_DELETE)

        self.assertNotEquals(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123456"
        )

        self.client.force_login(self.user)

        for _ in range(3):
            get_user_model().objects.create(
                username=f"test{_}",
                password="test123456",
                license_number=f"LIC1234{_}"
            )

    def test_retrieve_driver_list(self):
        response = self.client.get(DRIVER_LIST)

        users = get_user_model().objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["driver_list"]),
            list(users)
        )

    def test_retrieve_driver_create(self):
        response = self.client.get(DRIVER_CREATE)

        self.assertEquals(response.status_code, 200)

    def test_create_user(self):
        form_data = {
            "username": "new_user",
            "password1": "user123456",
            "password2": "user123456",
            "license_number": "LIC12345",
            "first_name": "User first",
            "last_name": "User last"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)

        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEquals(new_user.first_name, form_data["first_name"])
        self.assertEquals(new_user.last_name, form_data["last_name"])
        self.assertEquals(new_user.license_number, form_data["license_number"])

    def test_search_by_username_driver(self):
        get_user_model().objects.create(
            username="new_user",
            password="test123456",
            license_number="LIC12344"
        )

        response = self.client.get(DRIVER_LIST + "?username=test")

        self.assertNotContains(response, "new_user")
        self.assertContains(response, 'name="username" value="test"')

    def test_search_by_username_pagination(self):
        for _ in range(15):
            license_number = f"LIC1235{_}" if _ < 10 else f"LIC123{_}"

            get_user_model().objects.create(
                username=f"new_user_{_}",
                password="test123456",
                license_number=license_number
            )

        response = self.client.get(DRIVER_LIST + "?username=new&page=2")

        self.assertNotContains(response, "test1")
        self.assertContains(response, 'name="username" value="new"')
        self.assertContains(response, "new_user_5")

    def test_retrieve_driver_detail(self):
        response = self.client.get(DRIVER_DETAIL)

        self.assertEquals(response.status_code, 200)

    def test_retrieve_driver_update(self):
        response = self.client.get(DRIVER_LICENSE_UPDATE)

        self.assertEquals(response.status_code, 200)

    def test_retrieve_driver_delete(self):
        response = self.client.get(DRIVER_DELETE)

        self.assertEquals(response.status_code, 200)
