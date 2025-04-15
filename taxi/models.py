from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db.models import Q


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]
        verbose_name = "manufacturer"
        verbose_name_plural = "manufacturers"

    def __str__(self):
        return f"{self.name} {self.country}"

    @classmethod
    def search(cls, query):
        """Search manufacturers by name (case-insensitive)"""
        return cls.objects.filter(name__icontains=query)


class Driver(AbstractUser):
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["username"]
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})

    @classmethod
    def search(cls, query):
        """Search drivers by username, name, or license number"""
        return cls.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(license_number__icontains=query)
        ).order_by("username")


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(Driver, related_name="cars")

    class Meta:
        ordering = ["model"]

    def __str__(self):
        return self.model

    @classmethod
    def search(cls, query):
        """Search cars by model or manufacturer name"""
        return cls.objects.filter(
            Q(model__icontains=query) |
            Q(manufacturer__name__icontains=query)
        ).select_related("manufacturer").order_by("model")
