import random
import numpy as np
from distance import distance
import settings
import random_path

EXIT_CHOICES = (15, 16, 17)


# TODO 改正楼梯信息
# TODO 考虑楼梯的宽度


class Gene(object):
    """
    用于表示一个人的行为，包括他的四次选择，以及他到出口的距离
    变异方式：对每一位独立进行变异，变异概率由MUTATE_THRESHOLD控制
    交配方式：对基因进行整体杂交，因为方案中是每个人为单位，也就表示两个人完全互换选择
    """
    # MUTATE_THRESHOLD = 0.005, 0.01, 0.03, 0.1  # 第1、2、3、4次选择的变异概率
    MUTATE_THRESHOLD = settings.MUTATE_THRESHOLD  # 第1、2、3、4次选择的变异概率
    MATE_THRESHOLD = settings.MATE_THRESHOLD  # 交配的概率
    # MATE_THRESHOLD = 0.01  # 交配的概率
    DISTANCE = distance

    _cache = dict()

    def __init__(self, index, x, y, speed=1.5, start_time=0):
        """
        :param index: 参数中的index都代表楼层，其中2层为index=0，-1层为index=3，不需要-2层
        :param position: 一个人员单元的索引
        """
        self.index = np.int_(index)
        self.position = np.array((x, y), np.float_)
        self.speed = np.float_(speed)
        self.choice = np.array(random_path.get_random(index, (x, y)), np.intc)
        self.start_time = start_time

    def set_choices(self, *args):
        self.choice = np.array(args)

    @property
    def distance(self):
        item = (*self.position, *self.choice)
        if item in self._cache:
            return self._cache[item]
        result = np.zeros((5,), np.float_)
        position = tuple(self.position)
        if self.index == 0:
            result[0] = distance[position, self.choice[0]]
            result[1] = distance[self.choice[0], self.choice[1]]
            result[2] = distance[self.choice[1], self.choice[2]]
            result[3] = distance[self.choice[2], self.choice[3]]
            result[4] = distance[self.choice[3], 14]
        elif self.index == 1:
            result[1] = distance[position, self.choice[1]]
            result[2] = distance[self.choice[1], self.choice[2]]
            result[3] = distance[self.choice[2], self.choice[3]]
            result[4] = distance[self.choice[3], 14]
        elif self.index == 2:
            result[2] = distance[position, self.choice[2]]
            result[3] = distance[self.choice[2], self.choice[3]]
            result[4] = distance[self.choice[3], 14]
        elif self.index == 3:
            result[3] = distance[position, self.choice[3]]
            result[4] = distance[self.choice[3], 14]
        else:
            raise ValueError('Wrong index.')

        self._cache[item] = result
        return result

    def mutate(self):
        """
        变异，按照每一位的变异概率，对每一位进行变异
        :return:
        """
        if random.random() < self.MUTATE_THRESHOLD:
            self.choice = random_path.get_random(self.index, self.position)

    _exists_11111 = np.array((True, True, True, True, True))
    _exists_01111 = np.array((False, True, True, True, True))
    _exists_00111 = np.array((False, False, True, True, True))
    _exists_00011 = np.array((False, False, False, True, True))
    _exists_11100 = np.array((True, True, True, False, False))
    _exists_01100 = np.array((False, True, True, False, False))
    _exists_00100 = np.array((False, False, True, False, False))

    @property
    def exists(self):
        if self.index == 0:
            if self.choice[2] in settings.EXIT_CHOICES:
                return self._exists_11100.copy()
            else:
                return self._exists_11111.copy()
        if self.index == 1:
            if self.choice[2] in settings.EXIT_CHOICES:
                return self._exists_01100.copy()
            else:
                return self._exists_01111.copy()
        if self.index == 2:
            if self.choice[2] in settings.EXIT_CHOICES:
                return self._exists_00100.copy()
            else:
                return self._exists_00111.copy()
        if self.index == 3:
            return self._exists_00011.copy()

    @classmethod
    def mate(cls, obj1: 'Gene', obj2: 'Gene', exchange=True):
        """
        完整交换两个基因的数据，也就是两个人完全交换选择的路径
        :return:
        """
        if random.random() < cls.MATE_THRESHOLD:
            if exchange:
                obj1.choice, obj2.choice = obj2.choice, obj1.choice
            else:
                obj2.choice = obj1.choice

    def __str__(self):
        choices = list(map(str, self.choice))
        choices = ', '.join(choices)
        x, y = self.position
        x = int(x)
        y = int(y)
        return f'{2 - self.index}层({x},{y}):[{choices}]'

    def __repr__(self):
        return str(self)

    @property
    def plot_position(self):
        x, y = self.position
        plot_y = self.index * 100
        if y == 0:
            plot_x = x
        elif y == 220:
            plot_x = 1150 - x
        elif y == 35:
            plot_x = 1150 + x - 465
        elif y == 185:
            plot_x = 1600 - x + 465
        elif x == 465:
            plot_x = 465 + y
        elif x == 615:
            plot_x = 1300 + y - 35
        else:
            plot_x = 0
        return plot_x, plot_y

    def clone(self):
        obj = Gene(self.index, *self.position, self.speed, self.start_time)
        obj.choice = self.choice
        return obj


if __name__ == '__main__':
    pass
