from trianglesolver import solve, degree
import math


class Triangulate():
    def __init__(self) -> None:
        pass

    def __abs__(self):
        return self.string
    
    def object_size(self, dist, left_properties, right_properties):
        # Left camera min value
        left_angle = left_properties["r_angle"]

        # Right camera max value
        right_angle = right_properties["l_angle"]


        a, b = self.common_point(dist, left_angle, right_angle)
        print("common points: ",a,b)
        w, dist_to_object_l = self.width(left_properties, a)
        d, dist_to_object_r = self.depth(right_properties, b)
        h = self.height(left_properties, right_properties, dist_to_object_l, dist_to_object_r)
        return w, d, h


    def common_point(self, dist, left_angle, right_angle):
        A = 45 - abs(left_angle)
        B = 45 - abs(right_angle)
        print(f"common point: A: {A}, B: {B}, Dist: {dist}, r-l angle", left_angle,right_angle)
        a,b,c,A,B,C = solve(c=dist, A=A*degree, B=B*degree)
        return a,b # a = right cam, b = left cam
    
    def width(self, cam_properties, dist): # Left cam
        left_angle = cam_properties["l_angle"]
        right_angle = cam_properties["r_angle"]
        object_angle =  abs(left_angle - right_angle)

        # Assuming orthogonal placement
        C = object_angle
        A = 90 - abs(right_angle)
        B = 90 - abs(left_angle)
        b = dist

        a,b,c,A,B,C = solve(C=C*degree,B=B*degree,b=b)

        depth = c
        dist_to_object = math.sin(A)*b 
        return depth, dist_to_object

    def depth(self, cam_properties, dist):
        left_angle = cam_properties["l_angle"]
        right_angle = cam_properties["r_angle"]
        object_angle =  abs(left_angle - right_angle)

        # Assuming orthogonal placement
        C = object_angle
        A = 90 - abs(left_angle)
        B = 90 - abs(right_angle)
        b = dist
        print(A,B,b,C)

        a,b,c,A,B,C = solve(C=C*degree,B=B*degree,b=b)

        width = c
        print(width)
        dist_to_object = math.sin(A)*b 
        return width, dist_to_object
    
    def height(self, left_properties, right_properties, dist_l, dist_r):
        # left_cam 
        l_top = self.calc_height(left_properties['top_angle'], dist_l)
        l_bottom = self.calc_height(left_properties['bottom_angle'], dist_l)
        left_height = l_top + l_bottom

        # right_cam
        r_top = self.calc_height(right_properties['top_angle'], dist_r)
        r_bottom = self.calc_height(right_properties['bottom_angle'], dist_r)
        right_height = r_top + r_bottom
        print(f"left height: {left_height} right height: {right_height}")
        print(f"left: top angle: {left_properties['top_angle']} bottom angle: {left_properties['bottom_angle']} dist: {dist_l}")
        print(f"right: top angle: {right_properties['top_angle']} bottom angle: {right_properties['bottom_angle']} dist: {dist_r}")


        if(left_height > right_height):
            return left_height
        else:
            return right_height
    
    def calc_height(self, B, a):
        c = a * math.tan(math.radians(abs(B)))
        return c
