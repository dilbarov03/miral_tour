from django.db import models


class TourManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)
