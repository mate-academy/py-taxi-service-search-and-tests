from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.country})"

    def get_absolute_url(self):
        return reverse("taxi:manufacturer-list")


class Driver(AbstractUser):
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["username"]
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", args=[str(self.id)])

    def __str__(self):
        return self.username


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="cars",
    )

    class Meta:
        ordering = ["manufacturer"]

    def __str__(self):
        if self.manufacturer.name.split()[0] in self.model:
            return self.model
        return f"{self.manufacturer.name} {self.model}"

    def get_absolute_url(self):
        return reverse("taxi:car-detail", args=[str(self.id)])
