import settings
import random
import people_db
from distance import distance

_CHOICE_0, _CHOICE_1, _CHOICE_2, _CHOICE_3 = [tuple(settings.CHOICES[i].keys()) for i in range(4)]
_CHOICE_3_WITH_0 = (*_CHOICE_3, 0)

_sort_key = lambda item: item[1]


def _check_one_choice(index, previous, current):
    if previous in settings.EXIT_CHOICES:
        return current == 0
    if previous in settings.CHOICES[index]:
        return previous == current
    if previous == 0:
        return True
    return current != 0


def _check_choices(path):
    checks = (
        _check_one_choice(1, path[0], path[1]),
        _check_one_choice(2, path[1], path[2]),
        _check_one_choice(3, path[2], path[3]),
        any(path),
    )
    return all(checks)


def _calculate_distance(index, position, path):
    if index == 0:
        return sum((
            distance[position, path[0]],
            distance[path[0], path[1]],
            distance[path[1], path[2]],
            distance[path[2], path[3]],
            distance[path[3], 14],
        ))

    if index == 1:
        return sum((
            distance[position, path[1]],
            distance[path[1], path[2]],
            distance[path[2], path[3]],
            distance[path[3], 14],
        ))
    if index == 2:
        return sum((
            distance[position, path[2]],
            distance[path[2], path[3]],
            distance[path[3], 14],
        ))
    if index == 3:
        return sum((
            distance[position, path[3]],
            distance[path[3], 14],
        ))


def _generate_paths_of_one_person_at_0(position):
    paths1 = (
        (choice_0, choice_1, choice_2, choice_3)
        for choice_0 in _CHOICE_0
        for choice_1 in _CHOICE_1
        for choice_2 in _CHOICE_2
        for choice_3 in _CHOICE_3_WITH_0
    )
    paths2 = [path for path in paths1 if _check_choices(path)]
    paths3 = [(path, _calculate_distance(0, position, path)) for path in paths2]
    paths4 = sorted(paths3, key=_sort_key)[:settings.CHOICES_OF_ONE_PERSON]
    paths5 = [path for path, d in paths4]
    return paths5


def _generate_paths_of_one_person_at_1(position):
    paths1 = [
        (0, choice_1, choice_2, choice_3)
        for choice_1 in _CHOICE_1
        for choice_2 in _CHOICE_2
        for choice_3 in _CHOICE_3_WITH_0
    ]
    paths2 = [path for path in paths1 if _check_choices(path)]
    paths3 = [(path, _calculate_distance(1, position, path)) for path in paths2]
    paths4 = sorted(paths3, key=_sort_key)[:settings.CHOICES_OF_ONE_PERSON]
    paths5 = [path for path, d in paths4]
    return paths5


def _generate_paths_of_one_person_at_2(position):
    paths1 = [
        (0, 0, choice_2, choice_3)
        for choice_2 in _CHOICE_2
        for choice_3 in _CHOICE_3_WITH_0
    ]
    paths2 = [path for path in paths1 if _check_choices(path)]
    paths3 = [(path, _calculate_distance(2, position, path)) for path in paths2]
    paths4 = sorted(paths3, key=_sort_key)[:settings.CHOICES_OF_ONE_PERSON]
    paths5 = [path for path, d in paths4]
    return paths5


def _generate_paths_of_one_person_at_3(position):
    paths1 = [
        (0, 0, 0, choice_3)
        for choice_3 in _CHOICE_3_WITH_0
    ]
    paths2 = [path for path in paths1 if _check_choices(path)]
    paths3 = [(path, _calculate_distance(3, position, path)) for path in paths2]
    paths4 = sorted(paths3, key=_sort_key)[:settings.CHOICES_OF_ONE_PERSON]
    paths5 = [path for path, d in paths4]
    return paths5


def _generate_paths_of_one_person(index, position):
    if index == 0:
        return _generate_paths_of_one_person_at_0(position)
    if index == 1:
        return _generate_paths_of_one_person_at_1(position)
    if index == 2:
        return _generate_paths_of_one_person_at_2(position)
    if index == 3:
        return _generate_paths_of_one_person_at_3(position)


def _generate_paths():
    result = {
        (item['index'], item['x'], item['y']):
            _generate_paths_of_one_person(index=item['index'], position=(item['x'], item['y']))
        for item in people_db.read()
    }
    return result


_choices = _generate_paths()


def get_random(index, position):
    paths = _choices[(index, *position)]
    return random.choice(paths)


if __name__ == '__main__':
    with open('out.csv', mode='a', encoding='utf-8') as file:
        for choice, paths in _choices.items():
            for path in _choices[choice]:
                file.write(f'{choice[0]},{int(choice[1])},{int(choice[2])},{path[0]},{path[1]},{path[2]},{path[3]}\n')
            file.write('\n')
