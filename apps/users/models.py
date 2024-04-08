from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.users.managers import CustomUserManager


class User(AbstractUser, BaseModel):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.full_name or self.email


class SavedTour(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_tours", verbose_name=_("Пользователь"))
    tour = models.ForeignKey("tour.Tour", on_delete=models.CASCADE, verbose_name=_("Тур"),
                             related_name="saved_tours")

    class Meta:
        db_table = 'saved_tour'
        unique_together = ("user", "tour")
        verbose_name = _("Сохраненный тур")
        verbose_name_plural = _("Сохраненные туры")

    def __str__(self):
        return f"{self.user} - {self.tour}"
