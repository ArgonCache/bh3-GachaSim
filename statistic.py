import numpy as np
import matplotlib.pyplot as plt


def pre_sum(data, x):
    left = int(x)
    if left >= 200:
        return 1.0
    elif left < 0:
        return 0.0
    sum = data[0:left + 1].sum()
    sum += data[left + 1] * (x - left)

    return sum


def percentile(data, x):
    if x <= 0.0:
        return 0.0
    elif x >= 1.0:
        return 200.0
    left = 0
    right = 200
    while right - left > 1:
        median = int((right - left) / 2 + left)
        sum = data[0:median + 1].sum()
        if sum < x:
            left = median
        else:
            right = median
    sum = data[0:left + 1].sum()
    pos = left + (x - sum) / data[left + 1]

    return pos


if __name__ == '__main__':
    x = [i for i in range(201)]
    data = np.load('gacha.npy')
    exp = np.average(x, weights=data)
    var = np.average((x - exp) ** 2, weights=data)
    std = np.sqrt(var)
    mode = np.argmax(data)
    print("期望：", exp)
    print("标准差：", std)
    print("众数：", mode, "对应比例：", data[mode] * 100, "%")
    print("前50%抽数：", percentile(data, 0.5))
    print("前80%抽数：", percentile(data, 0.8))
    print("前95%抽数", percentile(data, 0.95))
    print("1个标准差范围：", exp - std, "~", exp + std, "占比：", (pre_sum(data, exp + std) - pre_sum(data, exp - std)) * 100,
          "%")
    print("2个标准差范围：", exp - 2 * std, "~", exp + 2 * std, "占比",
          (pre_sum(data, exp + 2 * std) - pre_sum(data, exp - 2 * std)) * 100, "%")
    print("3个标准差范围：", exp - 3 * std, "~", exp + 3 * std, "占比：",
          (pre_sum(data, exp + 3 * std) - pre_sum(data, exp - 2 * std)) * 100, "%")
    plt.plot(data)
    plt.show()
