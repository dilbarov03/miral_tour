from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel, File
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

    def delete(self, using=None, keep_parents=False):
        orders = self.orders.filter(status="moderation").annotate(persons_count=models.Count("persons"))
        for order in orders:
            if order.persons_count > 0:
                tour = order.tour
                tour.people_count += order.persons_count
                tour.save()
                person_files = order.persons.values_list("passport_file__id", flat=True)
                File.objects.filter(id__in=person_files).delete()
        super().delete(using, keep_parents)


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


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        MODERATION = "moderation", _("На модерации")
        PRE_PAYMENT = "pre_payment", _("В ожидании оплаты")
        SUCCESS = "success", _("Оплачен")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name=_("Пользователь"))
    tour = models.ForeignKey("tour.Tour", on_delete=models.CASCADE, verbose_name=_("Тур"),
                             related_name="orders")
    tarif = models.ForeignKey("tour.TourTarif", on_delete=models.CASCADE, verbose_name=_("Тариф"),
                              related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Общая стоимость"))
    status = models.CharField(max_length=20, verbose_name=_("Статус"), choices=OrderStatus.choices)
    order_file = models.FileField(verbose_name=_("Файл заказа"), upload_to="orders/", null=True, blank=True)

    class Meta:
        db_table = 'order'
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def __str__(self):
        return f"{self.user} - {self.tour}"


class OrderPerson(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="persons", verbose_name=_("Заказ"))
    full_name = models.CharField(max_length=255, verbose_name=_("ФИО"))
    passport_info = models.CharField(max_length=255, verbose_name=_("Паспортные данные"))
    passport_file = models.ForeignKey("common.File", on_delete=models.SET_NULL, verbose_name=_("Файл паспорта"),
                                      null=True)
    phone = models.CharField(max_length=15, verbose_name=_("Телефон"))
    email = models.EmailField(verbose_name=_("Email"))
    visa = models.BooleanField(default=False, verbose_name=_("Нужна виза"))
    order_call = models.BooleanField(default=False, verbose_name=_("Заказать звонок"))

    class Meta:
        db_table = 'order_person'
        verbose_name = _("Пассажир")
        verbose_name_plural = _("Пассажиры")

    def __str__(self):
        return f"{self.full_name} - {self.order}"
