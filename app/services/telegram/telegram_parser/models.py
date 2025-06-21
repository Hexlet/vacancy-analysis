from django.db import models

# Create your models here.


class Vacancy(models.Model):
    post = models.CharField(
        max_length=255, verbose_name=('vacancy_name'), blank=True, null=True
    )
    company = models.CharField(
        max_length=255, verbose_name=('company'), blank=True, null=True
    )
    city = models.CharField(
        max_length=255, verbose_name=('city'), blank=True, null=True
    )
    salary = models.CharField(
        max_length=255, verbose_name=('salary'), blank=True, null=True
    )
    link = models.CharField(
        max_length=255, verbose_name=('link'), blank=True, null=True
    )
    phone = models.CharField(
        max_length=25, verbose_name=('phone'), blank=True, null=True
    )
    busyness = models.CharField(
        max_length=25, verbose_name=('busyness'), blank=True, null=True
    )
    date = models.DateTimeField(verbose_name=('date'))

    def __str__(self):
        return self.post


class KeyWord(models.Model):
    post = models.CharField(
        max_length=255, verbose_name=('post'), blank=True, null=True
    )
    company = models.CharField(
        max_length=255, verbose_name=('company'), blank=True, null=True
    )
    salary = models.CharField(
        max_length=255, verbose_name=('salary'), blank=True, null=True
    )
    busyness = models.CharField(
        max_length=255, verbose_name=('busyness'), blank=True, null=True
    )
    city = models.CharField(
        max_length=255, verbose_name=('city'), blank=True, null=True
    )

    def __str__(self):
        return self.post
