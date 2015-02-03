#coding: utf-8

#--------------------------------------------------------------------------------------------------
import random
import string

def up_first_letter(st):
    if st:
        return st[0].upper() + st[1:]
    return st

def up_second_letter(st):
    if st:
        return st[0] + st[1].upper() + st[2:]
    return st


def rand(a, b):
    return random.randint(a, b)


def rand_item(list):
    return random.choice(list)


ALPHA_NUM = string.ascii_letters + string.digits
DIGITS = string.digits

def rand_seq(size, symbols=ALPHA_NUM):
    st = ""
    for i in range(size):
        st += random.choice(symbols)
    return st


def rand_log():
    logic = [False, True]
    return random.choice(logic)

#--------------------------------------------------------------------------------------------------

Vowels = [('a', 82), ('e', 127), ('i', 70), ('o', 75), ('u', 27), ('y', 20)]
Consonants = [('b', 15), ('c', 28), ('d', 43), ('f', 22), ('g', 20), ('h', 61), ('j', 1), ('k', 7), ('l', 40), ('m', 24), ('n', 68), ('p', 19), ('q', 1), ('r', 60), ('s', 63), ('t', 90), ('v', 10), ('w', 24), ('x', 1), ('z', 1)]


def rand_letter(vow_res):
    if vow_res:
        letters = Vowels
        num = rand(1, 401)
    else:
        letters = Consonants
        num = rand(1, 598)

    counter = 0
    for letter in letters:
        if num >= counter and num <= counter + letter[1]:
            return letter[0]
        counter += letter[1]

    return '*'


def rand_syllable():
    case = rand(0, 2)
    syllable = ""
    if case == 0:
        syllable = rand_letter(True) + rand_letter(False)

    if case == 1:
        syllable = rand_letter(False) + rand_letter(True)

    if case == 2:
        syllable = rand_letter(False) + rand_letter(True) + rand_letter(False)

    return syllable


def rand_word():
    word = ""
    length = rand(1, 4)
    for i in range(length):
        word += rand_syllable()
    return word


def rand_sentence(capitalize=True, ending="."):
    sentence = " "

    length = rand(3, 12)
    if ending == "?":
        length = rand(2, 5)
    
    for i in range(length):
        sentence = sentence + rand_word()
        if i < length - 1:
            sentence += " "

    if capitalize:
        sentence = up_second_letter(sentence)
    sentence += ending
    return sentence

#--------------------------------------------------------------------------------------------------

towns = ['Москва', 'Мурманск', 'Сочи', 'Омск', 'Тюмень', 'Волгоград', 'Астрахань',
         'Королев', 'Климовск', 'Химки', 'Люберцы', 'Новосибирск', 'Кемерово',
         'Ногинск', 'Пушкино', 'Щелково', 'Можайск', 'Обнинск', 'Калуга', 'Тверь', 'Вологда']

streets = ['Ленина', 'Сталина', 'Троцкого', 'Разина', 'Пушкина', 'Лермонтова', 'Тютчева',
          'Некрасова', 'Крокодилова', 'Русская', 'Каретная', 'Парковая', 'Перовской',
          'Суворова', 'Ушакова', 'Соколова', 'Пионеров', 'Коммунистов', 'Интернационалистов',
          'Шумилова', 'Бакунина', 'Зарайская', 'Сормовская', 'Камова', 'Мира', 'Ткацкая',
          'Хромова', 'Гражданская', 'Магистральная', 'Народная', 'Нагорная']

def get_address():
    town = rand_item(towns)
    street = rand_item(streets)
    house = rand(1, 100)
    return "г. %s, ул. %s, д. %s" % (town, street, str(house))

#--------------------------------------------------------------------------------------------------

UName = ['Иван', 'Петр', 'Николай', 'Семен', 'Максим', 'Сергей', 'Алексей', 'Михаил',
         'Дмитрий', 'Влад', 'Никита', 'Павел', 'Андрей', 'Адриан', 'Руслан', 'Владимир',
         'Кирилл', 'Борис', 'Глеб', 'Герман', 'Станислав', 'Георгий', 'Валерий']

UFamPre = ['Ву', 'Се', 'Петро', 'Мака', 'Ле', 'Мина', 'Мара', 'Ки', 'Фи', 'Ба', 'Дра', 'Мас']
UFamIn = ['п', 'х', 'т', 'к', 'ш', 'с', 'м', 'р', 'л', '']
UFamPost = ['ов', 'ев', 'ин', 'ан', 'ен', 'ян', 'ун', 'юн', 'ко', 'юк', 'як', 'ич']

def get_first_name():
    return rand_item(UName)

def get_surname():
    fampre = rand_item(UFamPre)
    famin = rand_item(UFamIn)
    fampost = rand_item(UFamPost)
    return fampre + famin + fampost

def get_full_name():
    return get_first_name() + ' ' + get_surname()

#--------------------------------------------------------------------------------------------------
UMailHost = ['yandex.ru', 'gmail.com', 'mail.ru', 'rambler.ru', 'yahoo.com']

def get_email():
    return rand_word() + '@' + rand_item(UMailHost)

def get_cellphone_number():
    return '9' + rand_seq(9, DIGITS)

#--------------------------------------------------------------------------------------------------
import os, sys
os.environ["DJANGO_SETTINGS_MODULE"] = "PersonsTable.settings"

from Table.models import Person
from django.db.utils import IntegrityError

PERSONS_AMOUNT = 1000

def fill_persons():
    i = 0
    while i < PERSONS_AMOUNT:
        person = Person()

        person.firstname = get_first_name()
        person.surname = get_surname()
        person.gender = 'M'

        person.address = get_address()
        person.email = get_email()
        person.phone = get_cellphone_number()

        try:
            person.save()
            i += 1
        except IntegrityError as ie:
            sys.stdout.write('-!-')

        sys.stdout.write('P')
        # print person
    print '\n'

def launch():
    fill_persons()
    print "DB was successfully filled"

launch()