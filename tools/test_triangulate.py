import unittest
from triangulate import Triangulate


class TestTriangulateClass(unittest.TestCase):

    def test_case_1(self): #object_size
        triangulate = Triangulate()
        left = {"l_angle":14.04,
        "r_angle":14.04}
        right = {"l_angle":14.04,
        "r_angle":14.04}
        dist = 35.36

        a, b = triangulate.object_size(dist, left, right)
        print(a,b)
        assert a is not None

    
    def test_case_2(self):
        triangulate = Triangulate()
        a, b = triangulate.common_point(dist=35.36, left_angle=14.04, right_angle=14.04)
        print(a,b)
        self.assertAlmostEqual(a, 20.62, 2)
        self.assertAlmostEqual(b, 20.62, 2)


if __name__ == '__main__':
    unittest.main()