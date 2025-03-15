from django.db import models
from django.utils.translation import gettext_lazy as _

from django_resized import ResizedImageField

from apps.common.models import BaseModel
from apps.tour.managers import TourManager


class Region(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название"))
    order = models.IntegerField(default=1, verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Регион")
        verbose_name_plural = _("Регионы")
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


class TourCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Название"))
    order = models.IntegerField(default=1, verbose_name=_("Порядок"))
    tour_type = models.ForeignKey(
        TourType,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name=_("Тип тура"),
        null=True
    )

    class Meta:
        verbose_name = _("Категория тура")
        verbose_name_plural = _("Категории туров")
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} - {self.tour_type}"


class TravelPeriods(models.TextChoices):
    ALL = "all", _("Весь год")
    WINTER = "winter", _("Зима")
    SPRING = "spring", _("Весна")
    SUMMER = "summer", _("Лето")
    AUTUMN = "autumn", _("Осень")


class Tour(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_("Slug"), null=True)
    description = models.TextField(verbose_name=_("Описание"), blank=True, null=True)
    main_image = ResizedImageField(upload_to="tours", verbose_name=_("Главное изображение"))
    category = models.ForeignKey(
        TourCategory,
        on_delete=models.CASCADE,
        related_name="tours",
        verbose_name=_("Категория"),
    )
    tour_type = models.ManyToManyField(
        TourType,
        related_name="tours",
        verbose_name=_("Тип тура"),
    )
    region_one = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="tours_region_one",
        verbose_name=_("Город 1"),
        null=True
    )
    region_two = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="tours_region_two",
        verbose_name=_("Город 2"),
        null=True
    )
    region_three = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="tours_region_three",
        verbose_name=_("Город 3"),
        null=True
    )
    region_four = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="tours_region_four",
        verbose_name=_("Город 4"),
        null=True,
        blank=True
    )
    region_five = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="tours_region_five",
        verbose_name=_("Город 5"),
        null=True,
        blank=True
    )
    period = models.CharField(max_length=255, choices=TravelPeriods.choices, verbose_name=_("Период"))
    days_count = models.IntegerField(verbose_name=_("Количество дней"), null=True)
    video_link = models.URLField(verbose_name=_("Ссылка на видео"), blank=True, null=True)
    video = models.FileField(upload_to="tour_videos", verbose_name=_("Видео"), blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Активный"))
    is_popular = models.BooleanField(default=False, verbose_name=_("Популярный"))
    people_count = models.IntegerField(verbose_name=_("Количество людей"))
    discount = models.BooleanField(default=False, verbose_name=_("Скидка"))
    discount_text = models.TextField(verbose_name=_("Текст скидки"), blank=True, null=True)

    objects = TourManager()

    class Meta:
        verbose_name = _("Тур")
        verbose_name_plural = _("Туры")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def min_price(self):
        return TourTarif.objects.filter(tour=self).aggregate(
            min_price=models.Min(
                models.Case(
                    models.When(models.Q(discount_price__isnull=False) & models.Q(tour__discount=True),
                                then="discount_price"),
                    default="price",
                )
            )
        )["min_price"]

    @property
    def origin_start_price(self):
        return TourTarif.objects.filter(tour=self).aggregate(
            min_price=models.Min("price")
        )["min_price"]


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
    subtitle = models.CharField(max_length=255, verbose_name=_("Подзаголовок"), blank=True, null=True)
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

    @property
    def final_price(self):
        return self.discount_price if self.tour.discount else self.price


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


class RegionTour(BaseModel):
    region = models.OneToOneField(Region, on_delete=models.CASCADE, related_name="region_tours",
                                  verbose_name=_("Регион"))
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="region_tours", verbose_name=_("Тур"))
    image = ResizedImageField(upload_to="region_tours", verbose_name=_("Изображение"))

    class Meta:
        verbose_name = _("Тур региона")
        verbose_name_plural = _("Туры регионов")

    def __str__(self):
        return f"{self.region} - {self.tour}"
