def get_ture_prob(prob):
    left = 0.0
    right = 1.0
    success = 0.0
    result = 0.0
    while abs(result - prob) > 1e-10:
        if result < prob:
            left = success
            success = (success + right) / 2
        else:
            right = success
            success = (success + left) / 2
        fail = 1 - success
        tmp = 1.0
        result = 0.0
        for i in range(1, 10):
            result += i * tmp
            tmp *= fail
        result *= success
        result += 10 * tmp
        result = 1 / result
    return success


if __name__ == '__main__':
    p1 = get_ture_prob(0.12396)
    p2 = get_ture_prob(0.15353)
    print('精准补给4星装备单抽概率（不含保底）：', p1)
    print('天命武库4星装备单抽概率（不含保底）：', p2)
