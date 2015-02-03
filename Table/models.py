from django.db import models

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

    def match_to(self, pattern):
        return pattern.match(self.fullname) or \
               pattern.match(str(self.birthdate)) or \
               pattern.match(self.gender) or \
               pattern.match(self.address) or \
               pattern.match(self.email) or \
               pattern.match(self.phone)