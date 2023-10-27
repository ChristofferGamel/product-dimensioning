import unittest
from app.triangulate import Triangulate


class TestTriangulateClass(unittest.TestCase):



    # def test_case_1(self): #object_size
    #     triangulate = Triangulate()
    #     left = {"l_angle":20.1217889816,
    #     "r_angle":-3.6993194923}
    #     right = {"l_angle":4.00404551,
    #     "r_angle":-19.2357271423}
    #     dist = 7.0710678119

    #     a, b, c = triangulate.object_size(dist, left, right)
        
    #     # self.assert_(a, not None)
    #     self.assertAlmostEqual(a, 2, 2)
    #     self.assertAlmostEqual(b, 2, 2)

    def test_width(self):
        triangulate = Triangulate()
        angles = {"l_angle":20, "r_angle":-20}
        dist = 5
        depth, dist_out = triangulate.width(angles, dist)
        print(depth, dist_out)
        self.assertAlmostEqual(depth, 3.42, 2)
        self.assertAlmostEqual(dist_out, 4.7, 2)
    
    
    def test_depth(self):
        triangulate = Triangulate()
        angles = {"l_angle":20, "r_angle":-20}
        dist = 5
        depth, dist_out = triangulate.depth(angles, dist)
        print(depth, dist_out)
        self.assertAlmostEqual(depth, 3.42, 2)
        self.assertAlmostEqual(dist_out, 4.7, 2)  

    def test_height(self):
        triangulate = Triangulate()
        left_properties = {"bottom_angle":25, "top_angle":-35}
        right_properties = {"bottom_angle":25, "top_angle":-35}
        dist_l = 5
        dist_r = 5

        height = triangulate.height(left_properties, right_properties, dist_l, dist_r)
        self.assertAlmostEqual(height, 5.83, 2) 


if __name__ == '__main__':
    unittest.main()