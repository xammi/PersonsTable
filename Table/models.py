from django.db import models

# Create your models here.


class Person(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    fullname = models.CharField(max_length=150)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField(auto_now_add=True)

    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.surname)

    def __str__(self):
        return "%s %s" % (self.firstname, self.surname)