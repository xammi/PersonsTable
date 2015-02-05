# coding: utf8
__author__ = 'max'

from django.forms import ModelForm
from Table.models import Person
import re


class AddPersonForm(ModelForm):
    reg_exps = {'fullname': ur'[А-ЯA-Z][а-яa-z]+ [А-ЯA-Z][а-яa-z]+',
                'gender': r'[MF]',
                'birthdate': r'\d{4}-\d{2}-\d{2}',
                'address': ur'г. [А-Я][а-я]+, ул. [А-Я][а-я]+, д. \d+',
                'email': r'\w+@\w+\.[a-z]+',
                'phone': r'\d{10}',
    }

    class Meta:
        model = Person
        fields = Person.fields()

    def is_valid(self):
        result = super(AddPersonForm, self).is_valid()

        for field in Person.fields():
            if not self.is_field_valid(field, self.data[field]):
                self.add_error(field, 'Invalid field: ')
                result = False

        return result

    def is_field_valid(self, field, value):
        match = re.search(self.reg_exps[field], value, re.UNICODE)
        return match