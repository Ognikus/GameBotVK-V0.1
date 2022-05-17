import random


class Slime:
    def __init__(self):
        self.name = 'Слизь'
        self.lvl_slime = random.randint(1, 10)
        self.reward_money = 3 * self.lvl_slime
        self.reward_exp = 5 * self.lvl_slime
        self.slime_damage = 5 * self.lvl_slime
        self.slime_hp = 20 * self.lvl_slime

class Goblin:
    def __init__(self):
        self.name = 'Гоблин'
        self.lvl_goblin = random.randint(10, 20)
        self.reward_money_g = 4 * self.lvl_goblin
        self.reward_exp_g = 6 * self.lvl_goblin
        self.goblin_damage = 6 * self.lvl_goblin
        self.goblin_hp = 25 * self.lvl_goblin