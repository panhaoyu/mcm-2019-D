import os
import glob
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d
import settings


def _get_base_path():
    base = settings.OUTPUT_DIRECTORY
    glob_obj = glob.glob(os.path.join(base, '*'))
    path_obj = [os.path.split(p)[1] for p in glob_obj]
    path_obj = [os.path.splitext(p)[0] for p in path_obj]
    path_obj = [int(p) for p in path_obj]
    path = max(path_obj) + 1
    path = str(path)
    path = os.path.join(settings.OUTPUT_DIRECTORY, path)
    return path


PATH = _get_base_path()


def _get_path(category, filename):
    directory = os.path.join(PATH, category)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, f'{filename}')


_data = {
    'time_hist': 1,
}


def draw_time_hist(time_list):
    fig = plt.figure()
    plt.hist(time_list, bins=40)
    plt.xlim(500, 1500)  # 用于设置坐标上下限
    plt.savefig(_get_path('时间直方图', f"{_data['time_hist']}png"))
    _data['time_hist'] += 1
    plt.close('all')


def draw_individual_time_of_every_person(data, generation, index):
    """
    data: [(1,2,300), (2, 3, 300), (x, y, z)]
    """
    ax = plt.subplot(projection='3d')
    for x, y, z in data:
        ax.bar3d(x, y, 0, dx=1, dy=1, dz=z)
    plt.savefig(_get_path(f'个体时间分布图/{generation}代', f'{index}.png'))


def write_time(time, generation):
    path = _get_path('data/time', 'min_time.txt')
    with open(path, mode='a', encoding='utf-8') as file:
        file.write(f'{min(time)}\n')
    path = _get_path('data/time', f'{generation}.txt')
    with open(path, mode='w', encoding='utf-8') as file:
        file.write('\n'.join(list(map(str, time))))


def write_individual(individual, generation):
    path = _get_path('data/individual', f'{generation}.csv')
    rows = [(2 - gene.index, *gene.position, gene.speed, gene.start_time, *gene.choice) for gene in individual]
    rows.insert(0, ['floor', 'x', 'y', 'spd', 'init time', 'choi 1', 'choi 2', 'choi 3', 'choi 4'])
    rows = [list(map(str, row)) for row in rows]
    rows = [','.join(row) for row in rows]
    content = '\n'.join(rows)
    with open(path, mode='w', encoding='utf-8') as file:
        file.write(content)
