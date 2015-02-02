from django.db import models

# Create your models here.


class Person(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField()

    address = models.CharField(max_length=128)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.IntegerField(max_length=10, unique=True)