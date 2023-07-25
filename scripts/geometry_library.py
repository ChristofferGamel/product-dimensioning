import math
# Expects degrees
# Returns degrees

def deg_to_rad(deg):
    return (deg * math.pi) / 180

def rad_to_deg(rad):
    return (rad * 180) / math.pi

class RightAngledTriangle():
    def __init__(self, a=None, b=None, c=None, A=None, B=None):
        self.a = a
        self.b = b
        self.c = c
        self.A = A
        self.B = B

    def calculate_missing_angles(self):
        if self.A is None:
            self.A = rad_to_deg(math.atan(self.a / self.b))
        elif self.B is None:
            self.B = 90 - self.A

    def calculate_missing_sides(self):
        if self.a is None:
            self.a = self.b * math.tan(deg_to_rad(self.A))
        elif self.b is None:
            self.b = self.a / math.tan(deg_to_rad(self.A))
        if self.c is None:
            self.c = math.sqrt(self.a**2 + self.b**2)

    def calculate_missing_values(self):
        self.calculate_missing_angles()
        self.calculate_missing_sides()

    def area(self):
        return 0.5 * self.a * self.b

class ArbitraryTriangle():
    def __init__(self, a=None, b=None, c=None, A=None, B=None, C=None):
        self.a = a
        self.b = b
        self.c = c
        self.A = A
        self.B = B
        self.C = C

    def calculate_missing_angles(self):
        if self.A is None:
            self.A = 180 - self.B - self.C
        elif self.B is None:
            self.B = 180 - self.A - self.C
        elif self.C is None:
            self.C = 180 - self.A - self.B

    def calculate_missing_sides(self):
        if self.a is None:
            if self.A is not None and self.c is not None and self.C is not None:
                self.a = math.sqrt(self.c**2 + self.A**2 - 2 * self.c * self.A * math.cos(deg_to_rad(self.C)))
        if self.b is None:
            if self.B is not None and self.a is not None and self.A is not None:
                self.b = self.a * math.sin(deg_to_rad(self.B)) / math.sin(deg_to_rad(self.A))
            elif self.B is not None and self.c is not None and self.C is not None:
                self.b = math.sqrt(self.c**2 + self.B**2 - 2 * self.c * self.B * math.cos(deg_to_rad(self.C)))
        if self.c is None:
            if self.a is not None and self.c is not None and self.A is not None:
                self.c = math.sqrt(self.a**2 + self.c**2 - 2 * self.a * self.c * math.cos(deg_to_rad(self.A)))
            elif self.b is not None and self.B is not None and self.C is not None:
                self.c = self.b * math.sin(deg_to_rad(self.C)) / math.sin(deg_to_rad(self.B))

    def calculate_missing_values(self):
        self.calculate_missing_angles()
        self.calculate_missing_sides()

    def area(self):
        if self.a is not None and self.b is not None and self.C is not None:
            return 0.5 * self.a * self.b * math.sin(deg_to_rad(self.C))
        elif self.a is not None and self.c is not None and self.B is not None:
            return 0.5 * self.a * self.c * math.sin(deg_to_rad(self.B))
        elif self.b is not None and self.c is not None and self.A is not None:
            return 0.5 * self.b * self.c * math.sin(deg_to_rad(self.A))
        else:
            return None
