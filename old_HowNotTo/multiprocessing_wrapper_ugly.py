from data import topology, start_point, end_point
from copy import copy
tplg = copy(topology)
tplg_classic = copy(topology)
import multiprocessing
import time
from PathFinder import PathFinder


print('have a look on https://docs.python.org/3.6/library/multiprocessing.html#multiprocessing-programming')
print('SECTION 17.2.3.2')
print ('EXPLICIT - wyrazny, jawny **** RAPPORT - porozumienie')


def returnus_outer():
    return 'returnus_outer'

def prepare_for_multiprocessing(topology, start_point):
    '''Creates iterable of possible directions while on start_point. Each iterable will be consumed by one process.
    Therefore, new start_point for each process will be different, and initial start_point info will be removed from graph
    Makes sense only if start point has more than one possible way to go. Otherwise it's just single process'''

    options_while_at_start_point = topology[start_point].keys()

    def remove_start_point_info_from_topology(topology, start_point):
        for crossroad in topology.items():
            crossroad_center = crossroad[0]
            crossroad_directions = crossroad[1].items()
            topology[crossroad_center] = {direction: time for direction, time in crossroad_directions if not direction == start_point}
        del topology[start_point]
        return topology

    topology = remove_start_point_info_from_topology(topology,start_point)
    return topology, options_while_at_start_point

'<<<<<<<<<<<<<< DONT <<<<<<<<<<< DONT <<<<<<<<<<<<<<<< DONT <<<<<<<<<<<<<'
    #following line is bad. it should be included in __main__procedure
#tplg_for_multiprocessing, initial_directions_for_multiprocessing = prepare_for_multiprocessing(tplg, start_point)
'<<<<<<<<<<<<<< DONT <<<<<<<<<<< DONT <<<<<<<<<<<<<<<< DONT <<<<<<<<<<<<<'


def solve_with_multiprocessing(derived_start_point):
    finished_paths = PathFinder(tplg, derived_start_point, end_point).solve()
    return list(map(lambda path: start_point + path, finished_paths))


if __name__ == '__main__':
    '<<<REF 1<<<<<<<< DONT <<<<<<<<<<< DONT <<<<<<<<<<<<<<<< DONT <<<<<<<<<<<<<'
    #following line also can not be here, as it will be not defined inside context manager
    topology_for_multiprocessing, initial_directions_for_multiprocessing = prepare_for_multiprocessing(tplg, start_point)
    '<<<REF 1<<<<<<< DONT <<<<<<<<<<< DONT <<<<<<<<<<<<<<<< DONT <<<<<<<<<<<<<'


    print('print in if __name__')
    startTime=time.time()
    # num_cores = multiprocessing.cpu_count()
    num_cores = 4
    with multiprocessing.Pool(num_cores) as p:
        tplg = copy(topology_for_multiprocessing) # REF 1 this is rather ugly, as it assigns potentially huge data
        results = p.map(solve_with_multiprocessing, initial_directions_for_multiprocessing)
        p.close()
        p.join()
        print(results)
    endTime=time.time()
    print ('MULTIPROCESSING TIME: {}'.format(endTime-startTime))

    #nie jestem pewien czemu print z poczatku skryptu (tplg_for_multiprocessing) wykonuje sie num_cores+1 razy
    #czyzby dla kazdego procesu interpreter od nowa analizowal caly skrypt?

    startTime = time.time()
    result_single = sorted(PathFinder(tplg_classic, start_point, end_point).solve())
    print(result_single)
    endTime = time.time()
    print ('CLASSIC TIME: {}'.format(endTime-startTime))
    print('CLASSIC SOLUTIONS AMOUNT: {}'.format(len(result_single)))
