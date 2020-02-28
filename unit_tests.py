from data import topology, start_point, end_point
from copy import copy
#from ver_Codewars import shortestPath
tplg = copy(topology)
tplg_classic = copy(topology)
#import multiprocessing
import time

import unittest
import multiprocessing_wrapper

result = ['jabdefcih', 'jabdefh', 'jabdeh', 'jabdgh', 'jacfedgh', 'jacfeh', 'jacfh', 'jacih', 'jaedgh', 'jaefcih', 'jaefh', 'jaeh', 'jaicfedgh', 'jaicfeh', 'jaicfh', 'jaih', 'jiabdefh', 'jiabdeh', 'jiabdgh', 'jiacfedgh', 'jiacfeh', 'jiacfh', 'jiaedgh', 'jiaefh', 'jiaeh', 'jicabdefh', 'jicabdeh', 'jicabdgh', 'jicaedgh', 'jicaefh', 'jicaeh', 'jicfeabdgh', 'jicfedgh', 'jicfeh', 'jicfh', 'jih']

class RecursiveSearch_MultiProcessing(unittest.TestCase):

    # def setUp(self) -> None:
    #     self.inst = recursive_multiprocessing.GraphSolver(topology, start_point, end_point)

    def test_temporary(self):
        temp_var = multiprocessing_wrapper.PathFinder(topology, start_point, end_point)
        self.assertNotEqual(temp_var, ['test'])

    def test_prepare_for_multiprocessing(self):
        print(topology[start_point])
        self.assertNotEqual(multiprocessing_wrapper.prepare_for_multiprocessing(topology, start_point)[0], topology)

    def test_returnus_outer(self):
        self.assertEqual(multiprocessing_wrapper.returnus_outer(), 'returnus_outer')

    def test_compute_path_time(self):
        print('https://stackoverflow.com/questions/326910/running-unit-tests-on-nested-functions')
        self.assertNotEqual(False,True)

    # def test_solve(self):
    #     self.assertEqual(self.inst.solve(), result)

if __name__ == '__main__':
    unittest.main()
