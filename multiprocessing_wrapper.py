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
    '''
    Creates iterable of possible directions while on start_point. Each iterable will be consumed by one process.
    Therefore, new start_point for each process will be different, and initial start_point info will be removed from graph
    Makes sense only if start point has more than one possible way to go. Otherwise it's just single process

    Another issue with function defined as below is that if it's called from context manager
    it will not know variables (tplg) defined outside the context manager.
    On the other hand if we put tplg inside context manager,
    it won't re-execute after the first run,
    as this function changes the object it operates on
    '''
       
    options_while_at_start_point = topology[start_point].keys()
    tmp_tplg = copy(topology)
    
    def remove_start_point_info_from_tmp_tplg(tmp_tplg, start_point):
        for crossroad in tmp_tplg.items():
            crossroad_center = crossroad[0]
            crossroad_directions = crossroad[1].items()
            tmp_tplg[crossroad_center] = {direction: time for direction, time in crossroad_directions if not direction == start_point}
        del tmp_tplg[start_point]
        return tmp_tplg

    tmp_tplg = remove_start_point_info_from_tmp_tplg(tmp_tplg,start_point)
    return tmp_tplg, options_while_at_start_point


def solve_with_multiprocessing(tplg_arg, derived_start_point):
    '''Let's force this function to use tplg as argument, instead of letting it operate on a global variable.
    This is for training purpose for applying harder pool.map logic (as the function will use iterable and a constant=tplg_arg)
    pool.starmap'''
    finished_paths = PathFinder(tplg_arg, derived_start_point, end_point).solve()
    return list(map(lambda path: start_point + path, finished_paths))


if __name__ == '__main__':
    tplg_arg, initial_directions_for_multiprocessing = prepare_for_multiprocessing(tplg, start_point)

    print('print in if __name__')
    startTime=time.time()
    # num_cores = multiprocessing.cpu_count()
    num_cores = 4
    with multiprocessing.Pool(num_cores) as p:
        results = p.starmap(solve_with_multiprocessing, zip([tplg_arg for i in range(len(initial_directions_for_multiprocessing))], initial_directions_for_multiprocessing))
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
