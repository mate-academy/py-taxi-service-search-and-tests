from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Topic

TOPIC_URL = reverse("taxi:topic-list")


class PublicTopicTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TOPIC_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTopicTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1",
        )
        self.client.force_login(self.user)

    def test_required_topics(self):
        Topic.objects.create(name="fff")
        Topic.objects.create(name="ccc")
        response = self.client.get(TOPIC_URL)
        self.assertEqual(response.status_code, 200)
        topics = list(Topic.objects.all())
        self.assertEqual(
            list(response.context["topic_list"]),
            topics,
        )
