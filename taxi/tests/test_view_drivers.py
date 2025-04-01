from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()
DRIVER_CREATE = reverse("taxi:driver-create")
DRIVER_LIST = reverse("taxi:driver-list")
DRIVER_DETAIL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_UPDATE = reverse("taxi:driver-update", kwargs={"pk": 1})
DRIVER_DELETE = reverse("taxi:driver-delete", kwargs={"pk": 1})

URL_LIST = [
    DRIVER_CREATE,
    DRIVER_LIST,
    DRIVER_DETAIL,
    DRIVER_UPDATE,
    DRIVER_DELETE
]


class PublicDriverTest(TestCase):
    def test_login_requirement_driver_url(self):
        """
        Test that unauthorized user can't get access any Driver page
        """
        for url in URL_LIST:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200)
                self.assertIn("/accounts/login/", response.url)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="test_password123"
        )
        self.client.force_login(self.user)

        User.objects.create(
            username="jonny.depth",
            first_name="jonny",
            last_name="Depth",
            password="test_password",
            license_number="12345678",
        )
        User.objects.create(
            username="lina.inverse",
            first_name="Lina",
            last_name="Inverse",
            password="test_password",
            license_number="ABC4578"

        )

    def test_authorized_user_driver_url(self):
        for url in URL_LIST:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_driver_create_post_success_url(self):
        """
        Test that create user back page to redirect
        """
        url = reverse("taxi:driver-create")
        response = self.client.post(
            url,
            data={
                "username": "Naix",
                "password1": "test_password",
                "password2": "test_password",
                "license_number": "AAB12345"
            }
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertTrue(User.objects.filter(username="Naix").exists())

    def test_driver_get_queryset_without_query(self):
        """
        Test search without parameters. Default query
        """
        response = self.client.get(DRIVER_LIST)
        object_list = response.context["object_list"]
        self.assertEqual(set(object_list), set(User.objects.all()))

    def test_driver_get_queryset_with_query(self):
        """
            Test search without parameters. Default with parameters
        """
        response = self.client.get(DRIVER_LIST + "?query=Lina")
        object_list = response.context["object_list"]
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].first_name, "Lina")
