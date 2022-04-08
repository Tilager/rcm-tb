from russian_names import RussianNames
from random import randint, randrange
from datetime import timedelta, datetime

def random_date(start, end):
    s = []
    while len(s) < 15:
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        datee = start + timedelta(seconds=random_second)
        if datee not in s:
            s.append(datee.date().strftime('%d-%m-%Y'))
    return s


def randNumbers():
    s = []

    while len(s) < 15:
        numb = '{}{}-{}{}-{}{}'.format(randint(1, 9), randint(0, 9),
                                       randint(0, 9), randint(0, 9),
                                       randint(0, 9), randint(0, 9))
        if numb not in s:
            s.append(numb)

    return s


def createPass():
    s = []

    while len(s) < 15:
        pas = '900{}'.format(randint(1000000, 9999999))
        if pas not in s:
            s.append(pas)

    return s


# name surname

rs = list(RussianNames(count=2, patronymic=False, name=False, gender=0))
rn = list(RussianNames(count=2, patronymic=False, surname=False, gender=0))
print(rs)
print(rn)

# print(createPass())
d1 = datetime.strptime('1/1/1975', '%m/%d/%Y')
d2 = datetime.strptime('1/1/1990', '%m/%d/%Y')
dates_birth = random_date(d1, d2)

d1 = datetime.strptime('1/1/2000', '%m/%d/%Y')
d2 = datetime.strptime('1/1/2010', '%m/%d/%Y')
dates_prim = random_date(d1, d2)

posts = [i for _ in range(3) for i in ['Бригадир', 'Каменщик', 'Маляр', 'Монтажник', 'Электрик'] ]
print(tuple(zip(rn, rs, randNumbers(), createPass())))