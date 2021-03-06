from django.db import models
import datetime

class Person(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    fullname = models.CharField(max_length=150)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField(default=datetime.datetime.now)

    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return "%s" % self.fullname

    def __str__(self):
        return "%s" % self.fullname

    def as_dict(self):
        return dict(fullname=self.fullname,
                    gender=self.gender,
                    birthdate=str(self.birthdate),
                    address=self.address,
                    email=self.email,
                    phone=self.phone)

    @staticmethod
    def fields():
        return ['fullname', 'gender', 'birthdate', 'address', 'email', 'phone']