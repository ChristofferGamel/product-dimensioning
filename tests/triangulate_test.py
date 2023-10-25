import unittest
from app.triangulate import Triangulate


class TestTriangulateClass(unittest.TestCase):



    def test_case_1(self): #object_size
        triangulate = Triangulate()
        left = {"l_angle":20.1217889816,
        "r_angle":-3.6993194923}
        right = {"l_angle":4.00404551,
        "r_angle":-19.2357271423}
        dist = 7.0710678119

        a, b, c = triangulate.object_size(dist, left, right)
        
        # self.assert_(a, not None)
        self.assertAlmostEqual(a, 2, 2)
        self.assertAlmostEqual(b, 2, 2)

    


if __name__ == '__main__':
    unittest.main()