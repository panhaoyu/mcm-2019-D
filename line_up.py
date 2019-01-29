import numpy
import settings
import random
import numpy as np

LINE_NUMBERS = 500
TIME_DOWNSTAIRS = 10  # 下楼所需要的时间
TIME_SPAN = 10
CHOICES = list(range(1, 18))
CHOICES_NUMBERS = 17


def _run_on_the_floor(src, dst, exists, distance, speed):
    """
    平面内跑动阶段，需要考虑以下几个参数：
        是否存在于本层
        跑速
    """
    dst[:] = src
    dst[exists] += np.divide(distance[exists], speed[exists])


def _line_up_one_stair(dst, stair_width):
    dst_temp = dst.copy()
    time_with_index = enumerate(dst_temp)
    time_with_index = sorted(time_with_index, key=lambda i: i[1])
    time_span = TIME_SPAN / stair_width
    previous = - time_span
    for index, current in time_with_index:
        if current - previous < time_span:
            current = previous + time_span
        dst[index] = current
        previous = current
    return dst


def _line_up_one_floor(src, dst, exists, choices, index):
    """
    排队阶段，需要考虑以下几个参数：
        是否存在于本层
        分别选择了哪个门
    """
    dst[:] = src
    temp = src.copy()[exists]
    choices = choices[exists]
    available_choices = settings.CHOICES[index]
    for choice in CHOICES:
        if choice not in available_choices:
            continue
        width = available_choices[choice]
        result = _line_up_one_stair(temp[choices == choice], width)
        temp[choices == choice] = result
    dst[exists] = temp


def _after_downstairs(src, dst, exists):
    """
    下楼阶段，需要考虑以下几个参数：
        是否存在于本层
    """
    dst[:] = src
    dst[exists] += TIME_DOWNSTAIRS


def line_up(
        distances: np.ndarray,  # 距离，5列
        choices: np.ndarray,  # 选择，4列
        exists: np.ndarray,  # 存在的层数，5列
        speeds: np.ndarray,  # 速度，1列
        time_start: np.ndarray,  # 开始时间，1列
) -> np.ndarray:
    time_array = np.zeros((LINE_NUMBERS, 13))

    exists_0, exists_1, exists_2, exists_3 = [exists[:, i] for i in range(4)]
    exists_4 = np.ones((LINE_NUMBERS,)).astype(np.bool_)
    exists_0_1 = np.array((exists_0, exists_1)).all(0)
    exists_1_2 = np.array((exists_1, exists_2)).all(0)
    exists_2_3 = np.array((exists_2, exists_3)).all(0)

    distance_0, distance_1, distance_2, distance_3, distance_4 = [distances[:, i] for i in range(5)]
    choices_0, choices_1, choices_2, choices_3 = [choices[:, i] for i in range(4)]
    time_0, time_1, time_2, time_3, time_4, time_5, time_6, time_7, time_8, time_9, time_10, time_11, time_12 = \
        [time_array[:, i] for i in range(13)]

    _run_on_the_floor(time_start, time_0, exists_0, distance_0, speeds)
    _line_up_one_floor(time_0, time_1, exists_0, choices_0, index=0)
    _after_downstairs(time_1, time_2, exists_0_1)

    _run_on_the_floor(time_2, time_3, exists_1, distance_1, speeds)
    _line_up_one_floor(time_3, time_4, exists_1, choices_1, index=1)
    _after_downstairs(time_4, time_5, exists_1_2)

    _run_on_the_floor(time_5, time_6, exists_2, distance_2, speeds)
    _line_up_one_floor(time_6, time_7, exists_2, choices_2, index=2)
    _after_downstairs(time_7, time_8, exists_2_3)

    _run_on_the_floor(time_8, time_9, exists_3, distance_3, speeds)
    _line_up_one_floor(time_9, time_10, exists_3, choices_3, index=3)
    _after_downstairs(time_10, time_11, exists_3)

    _run_on_the_floor(time_11, time_12, exists_4, distance_4, speeds)
    return time_12


def get_data():
    def get_one_distance():
        result = [random.random() * 200 for i in range(5)]
        for index, i in enumerate(result):
            if random.random() < 0.2:
                result[index] = 0
        return result

    def get_one_choice():
        return [random.randint(1, CHOICES_NUMBERS) for i in range(4)]

    distances = [get_one_distance() for i in range(LINE_NUMBERS)]
    distances = np.array(distances, np.intc)

    choices = [get_one_choice() for i in range(LINE_NUMBERS)]
    choices = np.array(choices, np.intc)

    exists = np.random.random((LINE_NUMBERS, 4))
    exists *= 2
    exists = exists.astype(np.intc)
    exists = exists.astype(np.bool_)

    speed = np.ones((LINE_NUMBERS, 1))
    # speed = np.random.random((LINE_NUMBERS, 1)) * 2 + 1

    time_start = np.random.random((LINE_NUMBERS, 1))
    time_start *= 10

    return distances, choices, exists, speed, time_start


if __name__ == '__main__':
    line_up(*get_data())
