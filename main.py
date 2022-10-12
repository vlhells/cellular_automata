import random
import datetime
import os
import time
import math
import itertools
from colorama import Fore, Style


# Представители и их спавн:
def spawn_representative(field, signature):
    bd = generate_bd()
    while bd >= datetime.datetime.today().date():
        bd = generate_bd()

    #print(bd)

    strength = random.randint(0, 100)
    x, y = generate_coords()

    #print(x, y)

    while field[x][y] != 0:
        x, y = generate_coords()

    #print(x, y)
    representatives.append({'x': x, 'y': y, 'bd': bd, 'strength': strength, 'signature': signature})
    field[x][y] = signature


def generate_bd():
    bd = datetime.date(random.randint(2000, 2022), random.randint(1, 12), random.randint(1, 28))
    return bd


def generate_coords():
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    return x, y


# Движение представителей:
def move(representative: dict, field: list, direction: int):
    x = representative['x']
    y = representative['y']
    this_field_value = field[x][y]
    field[x][y] = 0

    match direction:
        case 0:
            x += 1
        case 1:
            y += 1
        case 2:
            x -= 1
        case 3:
            y -= 1

    need = True
    if 0 < x < len(field) and 0 < y < 10:
        if field[x][y] == 0:
            representative['x'] = x
            representative['y'] = y
        elif field[x][y] == this_field_value:
            for d in representatives:
                if d['x'] == representative['x'] and d['y'] == representative['y']:
                    d['strength'] += 1
                if d['x'] == x and d['y'] == y and representative['x'] != x and representative['y'] != y:
                    d['strength'] += 1
        elif field[x][y] != 0 and field[x][y] != this_field_value:
            first_power = -999
            second_power = -888
            for d in representatives:
                if d['x'] == representative['x'] and d['y'] == representative['y']:
                    first_power = d['strength'] + math.pi * ((datetime.datetime.today().date() - d['bd']).days / 365)
                if d['x'] == x and d['y'] == y:
                    second_power = d['strength'] + math.pi * ((datetime.datetime.today().date() - d['bd']).days / 365)
            if first_power > second_power:
                field[representative['x']][representative['y']] = this_field_value
                field[x][y] = field[representative['x']][representative['y']]
            elif second_power > first_power:
                field[representative['x']][representative['y']] = field[x][y]
            need = False

    if need:
        field[representative['x']][representative['y']] = this_field_value


# Отрисовка поля:
def draw(field):
    print(10*"\n")  # Для красивой отрисовки (обновления поля) во время отладки.
    #os.system('CLS')
    for k in range(0, 10):
        for m in range(0, 10):
            if field[k][m] == 1:
                print(Fore.RED, end='')
            elif field[k][m] == 2:
                print(Fore.GREEN, end='')
            elif field[k][m] == 3:
                print(Fore.CYAN, end='')
            elif field[k][m] == 4:
                print(Fore.MAGENTA, end='')
            print(field[k][m], end=' ')
            print(Style.RESET_ALL, end='')
        print()

#print()
#print(i, one_counter, two_counter, three_counter, four_counter)


# Инициализация поля:
field = []
for i in range(1, 11):
    field.append([])
for j in field:
    while len(j) < 10:
        j.append(0)

representatives = []
one_counter = 0
two_counter = 0
three_counter = 0
four_counter = 0
spawn_i = 0

signatures = [1, 2, 3, 4]

# Цикл спавна:
while spawn_i < 40:
    signature = -999

    if one_counter >= 10 and 1 in signatures:
        signatures.remove(1)
    if two_counter >= 10 and 2 in signatures:
        signatures.remove(2)
    if three_counter >= 10 and 3 in signatures:
        signatures.remove(3)
    if four_counter >= 10 and 4 in signatures:
        signatures.remove(4)

    if len(signatures) != 0:
        signature = random.choice(signatures)

    spawn_representative(field, signature)

    match signature:
        case 1:
            one_counter += 1
        case 2:
            two_counter += 1
        case 3:
            three_counter += 1
        case 4:
            four_counter += 1

    spawn_i += 1


# Основной цикл:
i = 0
fractions = {'one': 0, 'two': 0, 'three': 0, 'four': 0}
while i < 100:
    seasons = [1, 2, 3, 4]
    season = 0
    if i > 0:
        season = itertools.cycle(seasons)
        for representative in representatives:
            if representative['signature'] == season:
                representative['strength'] *= 1.5
        random.shuffle(representatives)
        for representative in representatives:
            for n in range(representative['x'] - 1, representative['x'] + 1):
                for m in range(representative['y'] - 1, representative['y'] + 1):
                    if 0 < n < len(field) and 0 < m < len(field[n]):
                        direction = random.randint(0, 3)
                        move(representative, field, direction)
    draw(field)

    fractions['one'] = 0
    fractions['two'] = 0
    fractions['three'] = 0
    fractions['four'] = 0

    for f in field:
        fractions['one'] += f.count(1)
        fractions['two'] += f.count(2)
        fractions['three'] += f.count(3)
        fractions['four'] += f.count(4)
    print(fractions)

    for representative in representatives:
        if representative['signature'] == season:
            representative['strength'] /= 1.5

    i += 1
    time.sleep(1.5)  # Если выключить, то выведет результат почти сразу.


winner = max(fractions.values())
for i in fractions:
    if fractions[i] == winner:
        winner = i
        print('Победил народ:', i)
        break
