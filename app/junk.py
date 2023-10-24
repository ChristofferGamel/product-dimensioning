from triangulate import Triangulate

triangulate = Triangulate()
left = {"l_angle":14.04,
"r_angle":-14.04}
right = {"l_angle":14.04,
"r_angle":-14.04}
dist = 7.07

a, b, c = triangulate.object_size(dist, left, right)
print(a,b)