from datetime import date, datetime
from django.utils import timezone
import taxi
from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=2)

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("taxi:redactor-detail", kwargs={"pk": self.pk})


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=255, default="")
    published_date = models.DateField(default=date.today)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    publishers = models.ManyToManyField(Redactor, related_name="newspapers")

    def __str__(self):
        # return f"{self.title} ({self.content} {self.drivers})"
        return f"{self.title}"

