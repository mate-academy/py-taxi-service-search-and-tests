from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Newspaper, Topic


class ModelsTests(TestCase):
    def test_newspaper_str(self):
        newspaper_str = Newspaper(title="tests")
        self.assertEqual(str(newspaper_str), newspaper_str.title)

    def test_redactor_str(self):
        redactor = get_user_model().objects.create(
            username="test",
            first_name="test1",
            last_name="test2"
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username} ({redactor.first_name} {redactor.last_name})"
        )

    def test_topic_str(self):
        topic = Topic.objects.create(
            name="test",
        )
        self.assertEqual(
            str(topic),
            f"{topic.name}"
        )

    def test_create_redactor_with_years_of_experience(self):
        username = "test"
        years_of_experience = 23
        redactor = get_user_model().objects.create(
            username=username,
            years_of_experience=years_of_experience
        )
        self.assertEqual(redactor.username, username)
        self.assertEqual(redactor.years_of_experience, years_of_experience)
