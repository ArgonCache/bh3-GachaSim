import numpy as np
import matplotlib.pyplot as plt
import random


class Gacha:
    p = 0.04877
    p_weapon = 0.2 * p
    p_single_trace = 0.1 * p

    pos_weapon = p_weapon
    pos_top = pos_weapon + p_single_trace
    pos_middle = pos_top + p_single_trace
    pos_bottom = pos_middle + p_single_trace

    def __init__(self):
        self.num = 0
        self.floor_10 = 0
        self.floor_50 = 0
        self.weapon = 0
        self.top = 0
        self.middle = 0
        self.bottom = 0
        self.new_trace = 0
        self.completed = False
        self.star_4 = 0

    def get_one(self, pos):
        if pos < self.p:
            self.floor_10 = 0
            self.star_4 += 1
            if pos < self.pos_weapon:
                if self.weapon == 0:
                    self.floor_50 = 0
                self.weapon += 1
            elif pos < self.pos_top:
                if self.top == 0:
                    self.floor_50 = 0
                    self.new_trace += 1
                self.top += 1
            elif pos < self.pos_middle:
                if self.middle == 0:
                    self.floor_50 = 0
                    self.new_trace += 1
                self.middle += 1
            elif pos < self.pos_bottom:
                if self.bottom == 0:
                    self.floor_50 = 0
                    self.new_trace += 1
                self.bottom += 1

    def get_new_pos(self):
        max = self.p_single_trace * (3 - self.new_trace)
        if self.weapon == 0:
            max += self.p_weapon
        pos = random.uniform(0.0, max)
        if self.weapon != 0:
            pos += self.p_weapon
        if pos >= self.pos_weapon:
            if self.top != 0:
                pos += self.p_single_trace
            if pos >= self.pos_top and self.middle != 0:
                pos += self.p_single_trace

        return pos

    def single_gacha(self):
        self.num += 1
        self.floor_10 += 1
        self.floor_50 += 1

        if self.floor_50 == 50 and (self.weapon == 0 or self.new_trace < 3):
            self.get_one(self.get_new_pos())
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
            if self.weapon > 0:
                if self.new_trace == 3:
                    self.completed = True
                elif self.new_trace == 2 and self.top + self.middle + self.bottom >= 4:
                    self.completed = True


if __name__ == '__main__':
    x = [i for i in range(201)]
    y = np.zeros(201)
    for i in range(100000):
        gacha = Gacha()
        gacha.complete()
        y[gacha.num] += 1
    y = y / y.sum()
    np.save('gacha.npy', y)
    print('期望：', np.average(x, weights=y))
    plt.plot(y)
    plt.savefig('gacha.svg', dpi=600, format='svg')
    plt.show()
