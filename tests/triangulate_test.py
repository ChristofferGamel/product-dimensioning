import unittest
from app.triangulate import Triangulate


class TestTriangulateClass(unittest.TestCase):
    def test_e2e(self):
        triangulate = Triangulate()
        dist = 5.66
        left_properties = {"r_angle":-18.43,"l_angle":18.43,"top_angle":-18.43, "bottom_angle":18.43}
        right_properties = {"r_angle":-18.43,"l_angle":18.43,"top_angle":-18.43, "bottom_angle":18.43}
        w,d,h = triangulate.object_size(dist, left_properties, right_properties)
        
        self.assertAlmostEqual(w, 2, 2)
        self.assertAlmostEqual(d, 2, 2)
        self.assertAlmostEqual(h, 2, 2)

    def test_width(self):
        triangulate = Triangulate()
        angles = {"l_angle":20, "r_angle":-20}
        dist = 5
        depth, dist_out = triangulate.width(angles, dist)
        
        self.assertAlmostEqual(depth, 3.42, 2)
        self.assertAlmostEqual(dist_out, 4.7, 2)
    
    
    def test_depth(self):
        triangulate = Triangulate()
        angles = {"l_angle":20, "r_angle":-20}
        dist = 5
        depth, dist_out = triangulate.depth(angles, dist)
        
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