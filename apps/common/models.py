from django.db import models
from django.utils.translation import gettext_lazy as _

from django_resized import ResizedImageField


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Slide(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    text = models.TextField(null=True, blank=True, verbose_name=_("Текст"))
    image = ResizedImageField(upload_to='slides', verbose_name=_("Изображение"))
    order = models.IntegerField(verbose_name=_("Порядок"))

    class Meta:
        ordering = ['order']
        verbose_name = _("Слайд")
        verbose_name_plural = _("Слайды")

    def __str__(self):
        return self.title


class Statistics(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    subtitle = models.CharField(max_length=255, verbose_name=_("Подзаголовок"))
    value = models.CharField(verbose_name=_("Значение"), max_length=255)
    icon = models.FileField(upload_to='statistics', verbose_name=_("Иконка"))
    order = models.IntegerField(verbose_name=_("Порядок"))

    class Meta:
        ordering = ['order']
        verbose_name = _("Статистика")
        verbose_name_plural = _("Статистики")

    def __str__(self):
        return self.title


class NewsTag(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Название"))

    class Meta:
        verbose_name = _("Тег новости")
        verbose_name_plural = _("Теги новостей")

    def __str__(self):
        return self.name


class News(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    text = models.TextField(verbose_name=_("Текст"))
    image = ResizedImageField(upload_to='news', verbose_name=_("Изображение"), null=True, blank=True)
    tag = models.ForeignKey(NewsTag, on_delete=models.SET_NULL, related_name='news', verbose_name=_("Тег"), null=True)
    published_at = models.DateTimeField(verbose_name=_("Дата публикации"))

    class Meta:
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class MessageRequest(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Имя"))
    phone = models.CharField(max_length=15, verbose_name=_("Телефон"))
    message = models.TextField(verbose_name=_("Сообщение"))

    class Meta:
        verbose_name = _("Обратная связь")
        verbose_name_plural = _("Обратная связь")

    def __str__(self):
        return self.name


class Contact(BaseModel):
    latitude = models.FloatField(verbose_name=_("Широта"))
    longitude = models.FloatField(verbose_name=_("Долгота"))
    address = models.CharField(max_length=255, verbose_name=_("Адрес"))
    primary_phone = models.CharField(max_length=15, verbose_name=_("Основной телефон"))
    marketing_phone = models.CharField(max_length=15, null=True, verbose_name=_("Маркетинг телефон"))
    email = models.EmailField(verbose_name=_("Email"))
    instagram = models.URLField(null=True, verbose_name=_("Instagram"))
    youtube = models.URLField(null=True, verbose_name=_("YouTube"))
    facebook = models.URLField(null=True, verbose_name=_("Facebook"))
    telegram = models.URLField(null=True, verbose_name=_("Telegram"))

    class Meta:
        verbose_name = _("Контакт")
        verbose_name_plural = _("Контакты")

    def __str__(self):
        return self.address


class File(BaseModel):
    file = models.FileField(upload_to='files', verbose_name=_("Файл"))

    class Meta:
        verbose_name = _("Файл")
        verbose_name_plural = _("Файлы")

    def __str__(self):
        return self.file.name
