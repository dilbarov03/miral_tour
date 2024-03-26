from django.db import models
from django.utils.translation import gettext_lazy as _

from django_resized import ResizedImageField

from apps.common.models import BaseModel


class Region(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название"))
    order = models.IntegerField(default=1, verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Регион")
        verbose_name_plural = _("Регионы")
        ordering = ["order"]

    def __str__(self):
        return self.name


class TourCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название"))
    order = models.IntegerField(default=1, verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Категория тура")
        verbose_name_plural = _("Категории туров")
        ordering = ["order"]

    def __str__(self):
        return self.name


class TourType(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название"))
    image = ResizedImageField(upload_to="tour_types", verbose_name=_("Изображение"))
    order = models.IntegerField(default=1, verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Тип тура")
        verbose_name_plural = _("Типы туров")
        ordering = ["order"]

    def __str__(self):
        return self.name


class Tour(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    main_image = ResizedImageField(upload_to="tours", verbose_name=_("Главное изображение"))
    category = models.ForeignKey(
        TourCategory,
        on_delete=models.CASCADE,
        related_name="tours",
        verbose_name=_("Категория"),
    )
    tour_type = models.ForeignKey(
        TourType,
        on_delete=models.CASCADE,
        related_name="tours",
        verbose_name=_("Тип тура"),
    )
    from_region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="tours",
        verbose_name=_("Откуда")
    )
    to_region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="tours_to",
        verbose_name=_("Куда"),
    )
    return_region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="tours_return",
        verbose_name=_("Обратно"),
    )
    from_date = models.DateField(verbose_name=_("Дата начала"))
    to_date = models.DateField(verbose_name=_("Дата окончания"))
    video_link = models.URLField(verbose_name=_("Ссылка на видео"), blank=True, null=True)
    video = models.FileField(upload_to="tour_videos", verbose_name=_("Видео"), blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Активный"))
    people_count = models.IntegerField(verbose_name=_("Количество людей"))
    discount = models.BooleanField(default=False, verbose_name=_("Скидка"))
    discount_text = models.TextField(verbose_name=_("Текст скидки"), blank=True, null=True)

    class Meta:
        verbose_name = _("Тур")
        verbose_name_plural = _("Туры")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class TourImage(BaseModel):
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Тур"),
    )
    image = ResizedImageField(upload_to="tour_images", verbose_name=_("Изображение"))
    order = models.IntegerField(default=1, verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Изображение тура")
        verbose_name_plural = _("Изображения туров")
        ordering = ["order"]

    def __str__(self):
        return f"{self.tour} - {self.id}"


class TourDays(BaseModel):
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="days",
        verbose_name=_("Тур"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    text = models.TextField(verbose_name=_("Описание"))
    order = models.IntegerField(default=1, verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("День тура")
        verbose_name_plural = _("Дни туров")
        ordering = ["order"]

    def __str__(self):
        return f"{self.tour} - {self.order} - {self.title}"


class Feature(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    text = models.TextField(verbose_name=_("Описание"))
    file = models.FileField(upload_to="features", verbose_name=_("Файл"), blank=True, null=True)

    class Meta:
        verbose_name = _("Услуга")
        verbose_name_plural = _("Услуги")

    def __str__(self):
        return f"{self.title}"


class TourFeature(BaseModel):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="features", verbose_name=_("Тур"))
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="tours", verbose_name=_("Услуга"))
    included = models.BooleanField(default=True, verbose_name=_("Включено"))
    value = models.CharField(max_length=255, verbose_name=_("Значение"), blank=True, null=True)
    order = models.IntegerField(default=1, verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Услуга тура")
        verbose_name_plural = _("Услуги туров")
        ordering = ["order"]

    def __str__(self):
        return f"{self.tour} - {self.order}"


class TourTarif(BaseModel):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="tarifs", verbose_name=_("Тур"))
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена со скидкой"),
                                         blank=True, null=True)
    order = models.IntegerField(default=1, verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Тариф")
        verbose_name_plural = _("Тарифы")
        ordering = ["order"]

    def __str__(self):
        return f"{self.tour} - {self.title}"


class TarifFeature(BaseModel):
    tarif = models.ForeignKey(TourTarif, on_delete=models.CASCADE, related_name="features", verbose_name=_("Тариф"))
    included = models.BooleanField(default=True, verbose_name=_("Включено"))
    value = models.CharField(max_length=255, verbose_name=_("Значение"), blank=True, null=True)
    order = models.IntegerField(default=1, verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Услуга тарифа")
        verbose_name_plural = _("Услуги тарифов")
        ordering = ["order"]

    def __str__(self):
        return f"{self.tarif} - {self.order}"
