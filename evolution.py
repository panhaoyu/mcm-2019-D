import random
import individual
import settings
import plot

_sort_key = lambda ind: ind.fitness


def select(population):
    result = list()
    select_max = sorted(population, key=_sort_key)[:settings.SELECT_MAX]
    result.extend(select_max)
    select_times = int((settings.POPULATION_RANGE - settings.SELECT_MAX) / 4)
    for _ in range(select_times):
        random_list = [random.choice(population) for _ in range(5)]
        tmp = sorted(random_list, key=_sort_key)
        select_inds = tmp[:4]
        result.extend(select_inds)
    return result


def evolute(population):
    # time = [ind.time for ind in population]
    # mean_time = sum(time) / settings.POPULATION_RANGE

    # 选择
    population = select(population)
    population = [ind.clone() for ind in population]

    # 为下面准备
    sorted_population = sorted(population, key=_sort_key)
    good_individuals = sorted_population[:settings.SELECT_MAX]
    bad_individuals = sorted_population[settings.SELECT_MAX:]

    # 交配
    for _ in range(settings.MATE_NUMBER_COVER):  # 覆盖50次
        individual1 = random.choice(good_individuals)
        individual2 = random.choice(bad_individuals)
        individual.Individual.mate(individual1, individual2, exchange=False)
    for _ in range(settings.MATE_NUMBER_EXCHANGE):  # 杂交100次
        individual1 = random.choice(bad_individuals)
        individual2 = random.choice(bad_individuals)
        individual.Individual.mate(individual1, individual2)

    # 变异
    for ind in bad_individuals:
        ind.mutate()

    return population


def calculate(population):
    [ind.evaluate() for ind in population]
    return min([ind.fitness for ind in population])


def test_select():
    for _ in range(100):
        population = [individual.Individual() for _ in range(50)]
        new_population = select(population)
        assert calculate(population) <= calculate(new_population)


if __name__ == '__main__':
    population = [individual.Individual() for _ in range(settings.POPULATION_RANGE)]
    calculate(population)
    # while 1:
    for generation_index in range(1000000000):
        if settings.SAVE_TIME_HIST:
            plot.draw_time_hist([int(ind.fitness) for ind in population])
        plot.write_time([int(ind.fitness) for ind in population], generation_index)
        if settings.SAVE_INDIVIDUAL_DETAIL:
            [ind.draw(generation_index, index) for index, ind in list(enumerate(population))[:5]]
        plot.write_individual(sorted(population, key=_sort_key)[0], generation_index)
        population = evolute(population)
        min_time = calculate(population)
        print(min_time)
