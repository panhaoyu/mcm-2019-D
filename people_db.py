import settings
import csv

PATH = 'people_point.txt' if settings.LARGE_DATA else 'people_point2.txt'


def read():
    with open('people.csv', mode='r', encoding='utf-8') as file:
        fields = ('index', 'x', 'y', 'speed', 'start_time')
        reader = csv.DictReader(file, fieldnames=fields, delimiter=',')
        result = [i for i in reader][1:]
    for item in result:
        for key, value in item.items():
            item[key] = value.strip(' ')
        item['x'] = float(item['x'])
        item['y'] = float(item['y'])
        item['index'] = 2 - int(item['index'])
        item['speed'] = float(item['speed'])
        item['start_time'] = float(item['start_time'])
    return result


if __name__ == '__main__':
    import pprint
    import distance

    d = distance.Distance()

    for data in read():
        print(data)
    print(len(read()))
