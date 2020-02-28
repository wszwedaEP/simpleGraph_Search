from data import topology, start_point, end_point

def compute_path_time(path):
    '''Computes time for given path after its validated in GraphSolver'''
    def get_time(previous_step, next_step):
        return topology[previous_step][next_step]
    def get_next_pair_of_steps(path, iter_no):
        return path[iter_no], path[iter_no+1]

    time = 0
    for iter_no in range(len(path)):
        time += get_time(get_next_pair_of_steps(path, iter_no))

    return time

