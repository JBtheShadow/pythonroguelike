from random import randint, random


def from_dungeon_level(table, dungeon_level):
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0


def random_choice_index(chances):
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]


def dice_roll(amount=1, sides=6, modifier=None):
    running_sum = 0
    for _roll in range(amount):
        running_sum += randint(1, sides)
    
    if modifier:
        running_sum += modifier

    return running_sum


def random_range_decimal(low, high, modifier=None):
    if low > high:
        raise ValueError("low cannot be higher than high")
    
    if low == high:
        return low

    # Code only works if the value range's between 1 and N. For a low < 1 I need to shift the values first, then unshift them after the fact
    shift = 0
    if low < 1:
        shift = 1 - low
        low += shift
        high += shift

    amount = low
    sides = high / low

    running_sum = 0
    for _roll in range(amount):
        running_sum += random() * (sides - 1) + 1

    running_sum = round(running_sum)

    if modifier:
        running_sum += modifier

    if shift:
        running_sum -= shift

    return running_sum


def random_range(low, high, modifier=None):
    if low > high:
        raise ValueError("low cannot be higher than high")
    
    if low == high:
        return low

    # Code only works if the value range's between 1 and N. For a low < 1 I need to shift the values first, then unshift them after the fact
    shift = 0
    if low < 1:
        shift = 1 - low
        low += shift
        high += shift

    amount = low
    sides = high // low
    extra = high % low

    running_sum = dice_roll(amount - extra, sides) + dice_roll(extra, sides + 1)

    if modifier:
        running_sum += modifier

    if shift:
        running_sum -= shift

    return running_sum


if __name__ == "__main__":
    import numpy as np
    from matplotlib import pyplot as plt

    def test_random():
        print('A simple roll: {0}'.format(dice_roll()))
        print('2d8: {0}'.format(dice_roll(2, 8)))
        print('5d4-2: {0}'.format(dice_roll(5, 4, -2)))
        print('Range between 3 and 7 as if it were a dice roll: {0}'.format(random_range(3, 7)))
        print('Range between -5 and 5 as if it were a dice roll: {0}'.format(random_range(-5, 5)))
        print('Range between -5 and 5, plus 2, as if it were a dice roll: {0}'.format(random_range(-5, 5, 2)))
    test_random()

    def test_ranges():
        low = 4
        high = 12
        count = 100000
        data1 = [random_range_decimal(low, high) for random in range(count)]
        data2 = [random_range(low, high) for random in range(count)]

        bins = np.arange(low - 3, high + 3, 0.25)

        plt.figure(1)
        plt.xlim([min(data1)-1, max(data1)+1])
        plt.hist(data1, bins=bins, alpha=0.5)
        plt.title('Plot for {0} rolls of {1} to {2} with "decimal" dice'.format(count, low, high))
        plt.xlabel('roll result')
        plt.ylabel('count')

        plt.figure(2)
        plt.xlim([min(data2)-1, max(data2)+1])
        plt.hist(data2, bins=bins, alpha=0.5)
        plt.title('Plot for {0} rolls of {1} to {2} with normal dice'.format(count, low, high))
        plt.xlabel('roll result')
        plt.ylabel('count')

        plt.show()
    test_ranges()
