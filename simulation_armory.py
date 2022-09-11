import numpy as np
import matplotlib.pyplot as plt
import random


class Gacha:
    p = 0.0999936
    p_weapon = p * 13 / 80
    p_single_trace = p / 12

    pos_weapon_1 = p_weapon
    pos_weapon_2 = pos_weapon_1 + p_weapon
    pos_top = pos_weapon_2 + p_single_trace
    pos_middle = pos_top + p_single_trace
    pos_bottom = pos_middle + p_single_trace

    def __init__(self):
        self.num = 0
        self.floor_10 = 0
        self.floor_50 = 0
        self.weapon_1 = 0
        self.weapon_2 = 0
        self.top = 0
        self.middle = 0
        self.bottom = 0
        self.new_trace = 0
        self.completed = False
        self.star_4 = 0
        self.weapon_1_completed = 0
        self.weapon_2_completed = 0
        self.trace_completed = 0
        self.weapon_1_2_completed = 0
        self.weapon_1_trace_completed = 0
        self.weapon_2_trace_completed = 0

    def __getitem__(self, item):
        return getattr(self, item)

    def get_one(self, pos):
        if pos < self.p:
            self.floor_10 = 0
            self.star_4 += 1
            if pos < self.pos_weapon_1:
                if self.weapon_1 == 0:
                    self.floor_50 = 0
                self.weapon_1 += 1
            elif pos < self.pos_weapon_2:
                self.weapon_2 += 1
            elif pos < self.pos_top:
                if self.top == 0:
                    self.new_trace += 1
                self.top += 1
            elif pos < self.pos_middle:
                if self.middle == 0:
                    self.new_trace += 1
                self.middle += 1
            elif pos < self.pos_bottom:
                if self.bottom == 0:
                    self.new_trace += 1
                self.bottom += 1

    def single_gacha(self):
        self.num += 1
        self.floor_10 += 1
        self.floor_50 += 1

        if self.floor_50 == 50 and self.weapon_1 == 0:
            self.get_one(random.uniform(0.0, self.pos_weapon_1))
        elif self.floor_10 == 10:
            self.get_one(random.uniform(0.0, self.p))
        else:
            self.get_one(random.random())

    def single_gacha_without_floor_50(self):
        self.num += 1
        self.floor_10 += 1

        if self.floor_10 == 10:
            self.get_one(random.uniform(0.0, self.p))
        else:
            self.get_one(random.random())

    def complete(self):
        while not self.completed:
            self.single_gacha()

            if self.weapon_1_completed == 0 and self.weapon_1 > 0:
                self.weapon_1_completed = self.num
            if self.weapon_2_completed == 0 and self.weapon_2 > 0:
                self.weapon_2_completed = self.num
            if self.trace_completed == 0 and (
                    self.new_trace == 3 or (self.new_trace == 2 and self.top + self.middle + self.bottom >= 4)):
                self.trace_completed = self.num

            if self.weapon_1_completed > 0:
                if self.weapon_1_2_completed == 0 and self.weapon_2_completed > 0:
                    self.weapon_1_2_completed = self.num
                if self.weapon_1_trace_completed == 0 and self.trace_completed > 0:
                    self.weapon_1_trace_completed = self.num
            if self.weapon_2_trace_completed == 0 and self.weapon_2_completed > 0 and self.trace_completed > 0:
                self.weapon_2_trace_completed = self.num

            if self.weapon_1_2_completed > 0 and self.trace_completed > 0:
                self.completed = True


if __name__ == '__main__':
    # gacha = Gacha()
    # for i in range(100000000):
    #     gacha.single_gacha_without_floor_50()
    # print(gacha.num)
    # print(gacha.weapon_1)
    # print(gacha.weapon_2)
    # print(gacha.top)
    # print(gacha.middle)
    # print(gacha.bottom)
    # print(gacha.star_4)

    completed_name = ['num', 'weapon_1_completed', 'weapon_2_completed', 'trace_completed',
                      'weapon_1_2_completed', 'weapon_1_trace_completed', 'weapon_2_trace_completed']
    x = []
    y = {name: np.asarray([]) for name in completed_name}
    z = {name: [] for name in completed_name}
    for i in range(5000000):
        gacha = Gacha()
        gacha.complete()
        # print(gacha.weapon_1,gacha.weapon_2,gacha.top,gacha.middle,gacha.bottom)
        for name in completed_name:
            # print(gacha[name])
            z[name].append(gacha[name])
    for name in completed_name:
        z[name] = np.asarray(z[name])
        y[name] = np.bincount(z[name])
        y[name] = y[name] / y[name].sum()
        np.save('result/gacha_armory' + name + '.npy', y[name])
    for name in completed_name:
        x = [i for i in range(z[name].max() + 1)]
        print('期望：', np.average(x, weights=y[name]))
        plt.figure()
        plt.plot(y[name])
        plt.savefig('result/gacha_armory_' + name + '.svg', dpi=600, format='svg')
    plt.show()
