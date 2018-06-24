import random

def rolldice(number, sides):
    rolls = [random.randint(1, sides) for i in range(number)]
    return rolls

def attack(mat, defence, boost=False):
    if boost:
        atk_roll = sum(rolldice(3, 6))
    else:
        atk_roll = sum(rolldice(2, 6))

    if mat + atk_roll >= defence:
        return True
    else:
        return False

def dmg(power, arm, boost=False):
    if boost:
        dmg_roll = sum(rolldice(3, 6))
    else:
        dmg_roll = sum(rolldice(2, 6))

    if power + dmg_roll > arm:
        return power + dmg_roll - arm
    else:
        return 0


mat = 7
power = 13
defence = 10
arm = 19
boxes = 28

rounds = []
round_dmg = []
for i in range(1000):
    rboxes = boxes
    atks = []
    dmg_remain = []
    atk_num = 0
    while rboxes > 0:
        if attack(mat, defence):
            damage = dmg(power, arm)
            rboxes -= damage
        dmg_remain.append(rboxes)
        atk_num += 1
        atks.append(atk_num)
    rounds.append(atks)
    round_dmg.append(dmg_remain)






rounds = []
dmg = []
for i in range(100):
    rboxes = boxes
    atks = []
    dmg_remain = []
    atk_num = 0
    while rboxes > 0:
        attack = sum(rolldice(2, 6)) + pow
        if attack - arm > 0:
            rboxes -= attack - arm
        dmg_remain.append(rboxes)
        print(rboxes)
        atk_num += 1
        atks.append(atk_num)
    rounds.append(atks)
    dmg.append(dmg_remain)

r_length = [len(r) for r in rounds]

med_dmg = []
for i in range(max(r_length)):
    dmg_at_atk = []
    for d in dmg:
        try:
            dmg_at_atk.append(d[i])
        except IndexError:
            dmg_at_atk.append(0)

