# coding: utf8
__author__ = 'max'

from django import forms

class AddPersonForm(forms.Form):
    fullname = forms.CharField(label='ФИО', max_length=150)
    gender = forms.ChoiceField(label='Пол', widget=forms.CheckboxInput)
    birthdate = forms.DateField(label='Дата рождения')

    address = forms.CharField(label='Адрес', max_length=150)
    email = forms.EmailField(label='E-Mail')
    phone = forms.CharField(label='Телефон', max_length=10)

    # validators