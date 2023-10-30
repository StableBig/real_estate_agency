from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Flat(models.Model):
    new_building = models.BooleanField('Новостройка', null=True)
    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True)

    description = models.TextField('Текст объявления', blank=True)
    price = models.IntegerField('Цена квартиры', db_index=True)

    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True)
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное')
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж')

    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True)
    living_area = models.IntegerField(
        'Количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True)

    has_balcony = models.NullBooleanField('Наличие балкона', db_index=True)
    active = models.BooleanField('Активно ли объявление', db_index=True)
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True)

    liked_by = models.ManyToManyField(User, verbose_name='Кто лайкнул',
                                      related_name='liked_flats',
                                      blank=True
                                      )

    class Meta:
        verbose_name = 'Квартиру'
        verbose_name_plural = 'Квартиры'

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Complaint(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Кто жаловался',
        related_name='complaints'
    )
    flat = models.ForeignKey(
        Flat,
        on_delete=models.CASCADE,
        verbose_name='Квартира, на которую пожаловались',
        related_name='complaints'
    )
    text = models.TextField(
        'Текст жалобы'
    )

    class Meta:
        verbose_name = 'Жалобу'
        verbose_name_plural = 'Жалобы'

    def __str__(self):
        return self.complaint_text


class Owner(models.Model):
    name = models.CharField('ФИО владельца', max_length=200, db_index=True)
    phonenumber = models.CharField('Номер телефона владельца', max_length=20)
    pure_phone = PhoneNumberField('Нормализованный номер телефона владельца',
                                  region="RU", null=True, blank=True,
                                  )
    flats = models.ManyToManyField(Flat, related_name='owners',
                                   verbose_name='Квартиры в собственности',
                                   db_index=True
                                   )

    class Meta:
        verbose_name = 'Собственника'
        verbose_name_plural = 'Собственники'

    def __str__(self):
        return self.name
