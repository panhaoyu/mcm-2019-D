import numpy as np
import genes
import people_db
import settings
import line_up
import plot

PEOPLE = people_db.read()


class Individual(list):
    def __init__(self, *args, **kwargs):
        super(Individual, self).__init__(*args, **kwargs)
        if not self:
            for data in PEOPLE:
                gene = genes.Gene(**data)
                self.append(gene)
        self.time = np.zeros((len(self), 1))

    def evaluate(self):
        distances = np.array([i.distance for i in self], np.float_)
        choices = np.array([person.choice for person in self], np.intc)
        exists = np.array([person.exists for person in self], np.bool_)
        speeds = np.array([person.speed for person in self], np.float_)
        self.time = line_up.line_up(distances, choices, exists, speeds, self.time_start)

    @property
    def time_start(self):
        result = list()
        if settings.EMERGENCY_PERSONNEL_ENTRANCE:
            for person in self:
                if person.choice[2] == settings.EMERGENCY_PERSONNEL_DOOR:
                    result.append(person.start_time + settings.EMERGENCY_PERSONNEL_TIME_DELAY)
                else:
                    result.append(person.start_time)
        else:
            result.extend([person.start_time for person in self])
        result = np.array(result, np.float_)
        return result

    @property
    def fitness(self):
        max_time = max(self.time)
        return max_time

    def mutate(self):
        [person.mutate() for person in self]

    @classmethod
    def mate(cls, obj1, obj2, exchange=True):
        """
        exchange: 指定是否双方进行交换，False则由obj1覆盖obj2
        """
        for person1, person2 in zip(obj1, obj2):
            genes.Gene.mate(person1, person2, exchange=exchange)

    def __str__(self):
        return str(self.fitness)

    def __repr__(self):
        return str(self)

    def draw(self, generation, index):
        positions = [ind.plot_position for ind in self]
        data = zip(positions, self.time)
        data = [(*position, time) for position, time in data]
        plot.draw_individual_time_of_every_person(data, generation, index)

    def clone(self):
        return Individual([gene.clone() for gene in self])


def performance_test():
    for i in range(500):
        individual = Individual()
        individual.evaluate()


if __name__ == '__main__':
    import cProfile

    cProfile.run('performance_test()')
    input()
