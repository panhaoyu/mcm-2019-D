import settings

from settings import POSITIONS


class Distance(dict):
    def __getitem__(self, item):
        point1, point2 = item
        if point1 == 0:
            return 0
        if point2 == 0:
            return 0
        if point1 in settings.EXIT_CHOICES:
            return 1e20
        x1, y1 = point1 if isinstance(point1, tuple) else POSITIONS[point1]
        x2, y2 = point2 if isinstance(point2, tuple) else POSITIONS[point2]
        if item in self:
            return super(Distance, self).__getitem__(item)
        else:
            d = self._get_distance(x1, y1, x2, y2)
            self[item] = d
            return d

    def _get_distance(self, x1, y1, x2, y2):
        """
        point1->point2是一个有向线段
        :param point1:
        :param point2:
        :return:
        """

        if abs(y1 - y2) == 220:
            return 930 - x1 - x2 + 220
        if y1 - y2 == 0 and (0 <= x1 <= 465 and 0 <= x2 <= 465):
            return abs(x1 - x2)
        if y1 - y2 == 0 and (465 <= x1 <= 615 and 465 <= x2 <= 615):
            return abs(x1 - x2)
        # if y1 - y2 == 0:
        #     return abs(x1 - x2)
        if abs(y1 - y2) == 35:
            if y1 > y2:
                if y1 == 35:
                    return 35 - x2 + x1
                if y1 == 220:
                    return 35 + x2 - x1
            if y1 < y2:
                if y2 == 35:
                    return 35 - x1 + x2
                if y2 == 220:
                    return 35 + x1 - x2
        if abs(y1 - y2) == 185:
            if y1 > y2:
                if y1 == 185:
                    return 185 - x2 + x1
                if y1 == 220:
                    return 185 + x2 - x1
            if y1 < y2:
                if y2 == 185:
                    return 185 - x1 + x2
                if y2 == 220:
                    return 185 + x1 - x2
        if y1 == 220 and x2 == 465:
            return 465 - x1 + 220 - y2
        if y2 == 220 and x1 == 465:
            return 465 - x2 + 220 - y1
        if y1 == 0 and x2 == 465:
            return 465 - x1 + y2
        if y2 == 0 and x1 == 465:
            return 465 - x2 + y1
        # 1551 3553
        if y1 == 220 and x2 == 615:
            return 465 - x1 + 150 + 220 - y2
        if y2 == 220 and x1 == 615:
            return 465 - x2 + 150 + 220 - y1
        if y1 == 0 and x2 == 615:
            return 465 - x1 + 150 + y2
        if y2 == 0 and x1 == 615:
            return 465 - x2 + 150 + y1
        # 22
        if x1 == x2 == 465:
            return abs(y1 - y2)
        # 55
        if x1 == x2 == 615:
            return abs(y1 - y2)
        # 24
        if x1 == 465 and y2 == 185:
            return abs(y1 - y2) + x2 - 465
        if x2 == 465 and y1 == 185:
            return abs(y1 - y2) + x1 - 465
        if x1 == 465 and x2 == 615:
            if 0 <= y1 <= 35 or 185 <= y1 <= 220:
                return abs(y1 - y2) + 150
            if 35 < y1 < 185:
                return min((185 + 185 - y1 - y2), (y1 + y2 - 35 - 35)) + 150
        if x2 == 465 and x1 == 615:
            if 0 <= y2 <= 35 or 185 <= y2 <= 220:
                return abs(y1 - y2) + 150
            if 35 < y2 < 185:
                return min((185 + 185 - y1 - y2), (y1 + y2 - 35 - 35)) + 150
        # 26
        if x1 == 465 and y2 == 35:
            return abs(y1 - 35) + x2 - 465
        if x2 == 465 and y1 == 35:
            return abs(y2 - 35) + x1 - 465
        # 45
        if y1 == 185 and x2 == 615:
            return 185 - y2 + 615 - x1
        if y2 == 185 and x1 == 615:
            return 185 - y1 + 615 - x2
        # 46
        if y1 == 185 and y2 == 35:
            return min((x1 + x2 - 465 - 465), (615 + 615 - x1 - x2)) + 150
        if y2 == 185 and y1 == 35:
            return min((x1 + x2 - 465 - 465), (615 + 615 - x1 - x2)) + 150
        # 56
        if x1 == 615 and y2 == 35:
            return y1 - 35 + 615 - x2
        if x2 == 615 and y1 == 35:
            return y2 - 35 + 615 - x1
        # 71
        if y1 == 110 and y2 == 220:
            return min((abs(x2 - 365) + x1 - 365), (abs(x2 - 465) + 465 - x1)) + 110
        if y1 == 220 and y2 == 110:
            return min((abs(x1 - 365) + x2 - 365), (abs(x1 - 465) + 465 - x2)) + 110
        # 72
        if y1 == 110 and x2 == 465:
            return abs(y2 - 110) + 465 - x1
        if y2 == 110 and x1 == 465:
            return abs(y1 - 110) + 465 - x2
        # 73
        if y1 == 110 and y2 == 0:
            return min((abs(x2 - 365) + x1 - 365), (abs(x2 - 465) + 465 - x1)) + 110
        if y1 == 0 and y2 == 110:
            return min((abs(x1 - 365) + x2 - 365), (abs(x1 - 465) + 465 - x2)) + 110
        # 74
        if y1 == 110 and y2 == 185:
            return 75 + abs(x1 - x2)
        if y2 == 110 and y1 == 185:
            return 75 + abs(x1 - x2)
        # 75
        if y1 == 110 and 365 <= x1 <= 465 and x2 == 615:
            return min((185 - y2), (y2 - 35)) + 615 - x1 + 75
        if y2 == 110 and 365 <= x2 <= 465 and x1 == 615:
            return min((185 - y1), (y1 - 35)) + 615 - x2 + 75

        # 76
        if y1 == 110 and y2 == 35:
            return 75 + abs(x1 - x2)
        if y2 == 110 and y1 == 35:
            return 75 + abs(x1 - x2)
        # 77
        if y1 == y2 == 110:
            return abs(x1 - x2)


distance = Distance()

if __name__ == '__main__':
    distance = Distance()
    print(f' '.rjust(4), end=',')
    for i in range(1, 18):
        print(f'{i}'.rjust(4), end=',')
    print()
    for i in range(1, 18):
        print(f'{i}'.rjust(4), end=',')
        for j in range(1, 18):
            print(f'{distance[i, j]}'.rjust(4), end=',')
        print()
