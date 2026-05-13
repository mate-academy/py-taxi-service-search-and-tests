from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class PrivateDriverViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user_1 = user_model.objects.create_user(
            username="test1",
            password="test12345",
            first_name="first_test",
            last_name="last_test",
            license_number="ABC12345",
        )
        cls.user_2 = user_model.objects.create_user(
            username="test2",
            password="test12345",
            first_name="first_test",
            last_name="last_test",
            license_number="ABC54321",
        )

    def setUp(self):
        self.client.force_login(self.user_1)

    def test_search_driver_by_username(self):
        query = "test1"
        response = self.client.get(
            reverse("taxi:driver-list"),
            data={"q": query}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_1, response.context["object_list"])
        self.assertNotIn(self.user_2, response.context["object_list"])
