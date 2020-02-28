class PathFinder:
    def __init__(self, topology, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.tplg = topology

        self.next_step = None
        self.considered_path = None
        self.backtrack = [{self.start_point: [*self.tplg[self.start_point].keys()]}]
        self.history = self.start_point
        self.finished_paths = []

    def solve(self):

        def try_forward():

            get_next_step()
            self.considered_path = self.history + self.next_step

            if self.next_step == self.end_point:
                self.finished_paths.append(self.considered_path)
                try_backward()
            elif self.next_step not in self.history:
                clean_backtrack()
                add_new_crossroad_to_backtrack()
                self.history = self.considered_path
                try_forward()
            else:
                try_backward()

        def try_backward():
            clean_backtrack()
            try_forward()

        def returnus_inner():
            '''For unit_tests module test purpose'''
            return 'returnus_inner'

        def clean_backtrack():
            del list(self.backtrack[-1].values())[0][-1]
            directions_left_to_consider_at_last_path = list(self.backtrack[-1].values())[0]
            last_path = [*self.backtrack[-1].keys()][0]
            if not directions_left_to_consider_at_last_path and len(last_path) > 1:
                del self.backtrack[-1]
                last_path = [*self.backtrack[-1].keys()][0]
                self.history = last_path

        def add_new_crossroad_to_backtrack():
            self.backtrack.append({self.considered_path: [*self.tplg[self.next_step].keys()]})

        def get_next_step():
            self.next_step = list(self.backtrack[-1].values())[0][-1]

        def execute():
            try:
                try_forward()
            except IndexError:
                pass

        execute()

        return self.finished_paths