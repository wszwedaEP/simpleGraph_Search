from data import topology as tpl, start_point, end_point
from copy import copy


class GraphSolver:
    def __init__(self, topology, start_point, end_point):
        self.tplg = copy(topology)
        self.start_point = start_point
        self.end_point = end_point

        self.paths_explored = {}
        self.unexplored_paths = {self.start_point: [*self.tplg[self.start_point].keys()]}
        self.excluded_paths = []
        self.last_unexplored_path = self.start_point #this is questionable. should it be attribute?
        self.end_of_ends = False


    def check_if_dead_end(self, new_wp, wps_history, end_point):
        dead_end = True
        print('INSIDE CIDE. Possible waypoints: {}'.format(self.tplg[new_wp]))
        for poss_wp in self.tplg[new_wp]:
            print('INSIDE CIDE. new_wp: {} poss_wp: {} wps_history: {}'.format(new_wp,poss_wp, wps_history))
            if poss_wp not in wps_history:
                dead_end = False
        if new_wp == end_point:
            dead_end = False
        print('DEAD END: {}'.format(dead_end))
        return dead_end

    def get_previous_waypoint(self, path):
        try:
            return path[-2]
        except IndexError:
            return path[-1]

    def check_if_one_way_node(self, considered_waypoint, current_waypoint):
        one_way_node = True
        possible_waypoints = [*self.tplg[current_waypoint].keys()]
        possible_waypoints.remove(considered_waypoint)
        if len(possible_waypoints) > 1:
            one_way_node = False
        else:
            print ('<<<<ONE WAY NODE>>>>')
        return one_way_node

    def save_unexplored_path_info(self, considered_waypoint, wps_history, possible_waypoints):
        previous_crossroad = self.get_previous_waypoint(wps_history)
        considered_path = wps_history + considered_waypoint
        print('-----CROSSROAD MET------')
        valid_waypoints = [wp for wp in possible_waypoints if wp not in considered_path]
        print('VALID WPS {}'.format(valid_waypoints))
        if valid_waypoints:
            self.unexplored_paths[wps_history] = valid_waypoints
            print('UNXPL_PATH AS WPS_HISTORY {}'.format(wps_history))
            print('UNXPL_PATH AS SELF.UNXPL_PATH {}'.format(self.last_unexplored_path))
        else:
            print('-----CROSSROAD EXHAUSTED------')

    def update_unexplored_path_info(self, wps_history, new_wp):
        try:
            self.unexplored_paths[wps_history].remove(new_wp)
            if not self.unexplored_paths[wps_history]:
                del self.unexplored_paths[wps_history]
                print('DELETING EMPTY ENTRY IN UNEXPLORED PATHS. CURRENT FORM: {}'.format(self.unexplored_paths))

        except ValueError:
            pass

    def check_if_unexplored_paths_left(self, unexplored_paths):
        is_not_empty = False
        for unexplored_crossroad in unexplored_paths.values():
            if unexplored_crossroad:
                is_not_empty = True
        print('UNEXPLORED_PATHS_VALUES: {}'.format(unexplored_paths))
        print('IS NOT EMPTY: {}'.format(is_not_empty))
        return is_not_empty

    def get_rollback_to_last_valid_crossroad_if_needed(self, current_waypoint, last_unexplored_path, possible_waypoints):
        is_rollback_needed = False
        for poss_wp in possible_waypoints:
            if poss_wp not in last_unexplored_path:
                is_rollback_needed = True

        last_valid_path = last_unexplored_path.split(current_waypoint)[0]
        try:
            if not self.unexplored_paths[last_valid_path]:
                del self.unexplored_paths[last_valid_path]
                is_rollback_needed = True
                last_valid_path = sorted([*self.unexplored_paths.keys()], key=len)[0]

        except KeyError:
            pass

        if is_rollback_needed:
            current_waypoint = last_valid_path[-1]
            return current_waypoint, last_valid_path
        else:
            '/////ROLLBACK NOT NEEDED/////'
            return current_waypoint, last_unexplored_path

    def get_rollback_to_longest_unexplored_path_if_needed(self, current_waypoint, last_unexplored_path, unexplored_paths):
        if len(self.unexplored_paths.keys()) > 0:
            is_rollback_needed = False

            longest_unexplored_path = sorted([*self.unexplored_paths.keys()], key=len)[-1]
            last_waypoint_on_longest_unexplored_path = longest_unexplored_path[-1]
            possible_waypoints = self.tplg[last_waypoint_on_longest_unexplored_path]

            for poss_wp in possible_waypoints:
                if poss_wp not in longest_unexplored_path:
                    is_rollback_needed = True

            try:
                if not self.unexplored_paths[longest_unexplored_path]:
                    del self.unexplored_paths[longest_unexplored_path]
                    is_rollback_needed = True
            except KeyError:
                pass

            if is_rollback_needed:
                current_waypoint = longest_unexplored_path[-1]
                print('====ROLLBACK====')
                print('UNEXPLORED PATHS: {}'.format(self.unexplored_paths))
                print('CURR_WP: {} LONGEST PATH: {}'.format(current_waypoint,longest_unexplored_path))
                print('================')
                return current_waypoint, longest_unexplored_path
            else:
                '/////ROLLBACK NOT NEEDED/////'
                return current_waypoint, last_unexplored_path
        else:
            print ('++++KONIEC+++++++')
            self.end_of_ends = True
            return current_waypoint, last_unexplored_path


    def exclude_dead_parent_paths(self, last_valid_path, exhausted_path):
        last_valid_crossroad = last_valid_path[-1]
        print('EXHAUSTED PATH: {}'.format(exhausted_path))
        try:
            dead_part = exhausted_path[:-1].split(last_valid_crossroad)[1]
        except IndexError:
            dead_part = ''
        leftover = ''
        for wp in dead_part:
            leftover += wp
            considered_exclusion = last_valid_path + leftover
            if considered_exclusion not in self.excluded_paths:
                self.excluded_paths.append(last_valid_path+leftover)
            else:
                pass

    def run_algorithm(self):
        DBG_OUTER = 0
        DBG_INNER = 0
        wps_history = self.last_unexplored_path
        curr_wp = start_point
        previous_crossroad = False


        # external loop condition (repeat till there are no unexplored paths left)
        while self.check_if_unexplored_paths_left(self.unexplored_paths):  # temp_logic_inversion
            end_point_met_flag = False

            print('EXT_LOOP. PATHS EXPLORED: {}'.format(self.paths_explored))
            dead_ends = []

            DBG_OUTER += 1

            # internal loop condition (end point is met or previous crossroad is exhausted. this loop represents going down the graph)
            # leaving this loop means we need to rollback
            while not (previous_crossroad or end_point_met_flag or self.end_of_ends):
                DBG_INNER += 1
                print('\n')
                print('********************ITER {}**********************'.format(DBG_INNER))

                if wps_history in self.excluded_paths:
                    curr_wp, last_valid_path = self.get_rollback_to_longest_unexplored_path_if_needed(curr_wp,
                                                                                                      self.last_unexplored_path,
                                                                                                      self.unexplored_paths)
                    self.exclude_dead_parent_paths(last_valid_path,wps_history)
                    print('EXCLUDED PATHS: {}'.format(self.excluded_paths))
                    wps_history = last_valid_path
                    print('NEW WPS HISTORY: {}'.format(wps_history))


                print('CURR_WP: {}'.format(curr_wp))
                print('CURRENT PATH aka LAST_UNXPL_PATH: {}'.format(wps_history))
                # choose a path and store the info (including history)
                possible_wps = [*self.tplg[curr_wp].keys()] #a co gdyby possible waypoints nie brane byly z topologii, tylko z unexplored_paths
                #wtedy lipa. nie zmieniaj mapy, to byl twoj aksjomat
                print('POSSIBLE WPS: {}'.format(possible_wps))

                if wps_history in self.excluded_paths:
                    curr_wp, last_valid_path = self.get_rollback_to_longest_unexplored_path_if_needed(curr_wp,
                                                                                                      self.last_unexplored_path,
                                                                                                      self.unexplored_paths)

                for new_wp in possible_wps:

                    if wps_history+new_wp not in self.excluded_paths:
                        if not self.check_if_dead_end(new_wp, wps_history, self.end_point):
                            if new_wp not in wps_history:
                                print('CONSIDERED WP: {}'.format(new_wp))

                                "to potem w jedna funkcje"
                                if not self.check_if_one_way_node(new_wp, curr_wp):
                                    if wps_history not in self.unexplored_paths.keys():
                                        self.last_unexplored_path = wps_history
                                        if wps_history not in self.excluded_paths:
                                            self.save_unexplored_path_info(new_wp, self.last_unexplored_path, possible_wps)


                                try:
                                    self.update_unexplored_path_info(wps_history, new_wp)
                                    print('DELETED {}'.format(new_wp))
                                except KeyError:
                                    pass

                                wps_history += new_wp

                                curr_wp = new_wp
                                print('NEW PATH: {}'.format(wps_history))
                                print('UNEXPLORED PATHS: {}'.format(self.unexplored_paths))

                                if new_wp == end_point:
                                    exhausted_path = wps_history
                                    self.paths_explored[wps_history] = 'time TBC'
                                    curr_wp = self.get_previous_waypoint(self.last_unexplored_path)
                                    #curr_wp, last_valid_path = self.get_rollback_to_last_valid_crossroad_if_needed(curr_wp, self.last_unexplored_path, possible_wps)
                                    curr_wp, last_valid_path = self.get_rollback_to_longest_unexplored_path_if_needed(curr_wp, self.last_unexplored_path, self.unexplored_paths)
                                    self.exclude_dead_parent_paths(last_valid_path, exhausted_path)
                                    wps_history = last_valid_path
                                    print('-/-/- PATH EXHAUSTED. PATHS EXCLUDED: {}'.format(self.excluded_paths))
                                    end_point_met_flag = True

                                break

                            elif new_wp in wps_history:
                                continue
                        else:
                            dead_ends.append(new_wp)
                            print('@@@INSIDE DEAD END BLOCK. NEW_WP: {}'.format(new_wp))
                            if new_wp not in wps_history:
                                self.excluded_paths.append(wps_history)
                                self.excluded_paths.append(wps_history+new_wp)
                                try:
                                    self.update_unexplored_path_info(wps_history, new_wp)
                                except KeyError:
                                    pass
                                print('@@@INSIDE DEAD END BLOCK. PATHS EXCLUDED: {}'.format(self.excluded_paths))

                            continue

                    else:
                        continue

                if DBG_INNER > 107:
                    print(DBG_INNER)
                    break

            if DBG_OUTER > 50:
                print(DBG_OUTER)
                break



instance = GraphSolver(tpl, start_point, end_point)
instance.run_algorithm()
print('\n \n \n')
print('^^^^^^^^^^ THE END ^^^^^^^^^^^^')
print('PATHS EXPLORED: {}'.format(instance.paths_explored))
print('PATHS UNEXPLORED: {}'.format(instance.unexplored_paths))