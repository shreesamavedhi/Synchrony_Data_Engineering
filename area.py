import math
import filecmp
from os.path import exists
from pathlib import Path
import pandas as pd

################################ Sort the given points in counter-clockwise order ################################

def stringify_point(p):
    return str(p.x) + ',' + str(p.y)

def avg_points(pts):
        x = 0
        y = 0
        for i in range(0, len(pts)):
            x += pts[i].x;
            y += pts[i].y;
        return {'x': x/len(pts), 'y':y/len(pts)}

def sorted_points(points):
    # points = points[0]
    
    center = avg_points(points);

    angles = {};
    for i in range(0, len(points)):
        angles[stringify_point(points[i])] = math.atan2(points[i].x - center['x'], points[i].y - center['y']);

    points = sorted(points, key = lambda ele: angles[stringify_point(ele)])

    return points;

# Source: https://stackoverflow.com/questions/2855189/sort-latitude-and-longitude-coordinates-into-clockwise-ordered-quadrilateral
################################################################################################################

################ Helper Functions ################
def distSq(p, q):
    return ((p.x - q.x)**2 + (p.y - q.y)**2)**0.5

def angle(a, b, c):
    ang = math.degrees(math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x))
    return ang + 360 if ang < 0 else ang

def slope(p, q):
    dy = q.y - p.y 
    dx = q.x - p.x
    return dy/dx

# Function to calculate height of the trapezoid
def findHeight(p1, p2, b, c):
    a = max(p1, p2) - min(p1, p2)
    # Apply Heron's formula
    s = (a + b + c) // 2
    # Calculate the area
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    # Calculate height of trapezoid
    height = (area * 2) / a
    return height

####################################################

################ Shape Areas #######################
def square(side):
    return "Square " + str(side ** 2)

def rectangle(width, height):
    return "Rectangle " + str(width * height)

def parallelogram(side1, side2, angle):
    return "Parallelogram " + str(side1 * side2 * math.sin(angle))

def trapezoid(height, width_1, width_2):
    return "Trapezoid " + str(0.5 * height * ( width_1 + width_2 ))

def rhombus(height, width):
    return "Rhombus " + str(0.5 * height * width)

def kite(height, width):
    return "Kite " + str(0.5 * height * width)

####################################################

def shape(p1, p2, p3, p4):

    # sort points so that 
    points = [p1, p2, p3, p4]
    points.sort(key=lambda point: point.x)

    # four sides, two diagonals
    s1 = distSq(p1, p2)
    s2 = distSq(p2, p3)
    s3 = distSq(p3, p4)
    s4 = distSq(p4, p1)

    a1 = angle(p1, p2, p3)
    a2 = angle(p2, p3, p4)
    a3 = angle(p3, p4, p1)
    a4 = angle(p4, p1, p2)

    e1 = slope(p1, p2)
    e2 = slope(p2, p3)
    e3 = slope(p3, p4)
    e4 = slope(p4, p1)

    d1 = distSq(p1, p3)
    d2 = distSq(p2, p4)

    side_list = [s1, s2, s3, s4]
    angle_list = [a1, a2, a3, a4]
    slope_list = [e1, e2, e3, e4]
    diag_list = [d1, d2]

    # any invalid distances, return -1
    if ((i == 0 for i in side_list) or (j == 0 for j in angle_list)):
        return -1

    if (a1 == a2 == a3 == a4 == 90):
        if(s1 == s2 == s3 == s4):
            # Square: All interior angles are 90 degrees, All sides are equal
            return square(s1)
        else:
            # Rectangle: All interior angles are 90 degrees
            return rectangle(s1, s2)
    
    elif (e1 == e2 == e3 == e4):
        if (s1 == s2 == s3 == s4):
            # Rhombus: Two pairs of parallel sides, All sides are equal
            return rhombus(d1, d2)
        else:
            # Parallelogram: Two pairs of parallel sides
            return parallelogram(s1, s2, a1)
    elif (e1 == e3 or e2 == e4):
        if(e1 == e3):
            # Trapezoid: One pair of parallel sides
            height = findHeight(s2, s4, s1, s3)
            return trapezoid(height, s1, s3)
        else:
            # Trapezoid: One pair of parallel sides
            height = findHeight(s1, s3, s2, s4)
            return trapezoid(height, s2, s4)
    elif ( (s1 == s2 and s3 == s4 and s1 != s3) or (s2 == s3 and s4 == s1 and s2 != s4)):
        if (s1 == s2 and s3 == s4 and s1 != s3):
            # Kite: Two equal sides, pair must be adjacent and distinct
            return kite(d1, d2)
        else:
            # Kite: Two equal sides, pair must be adjacent and distinct
            return kite(d2, d1)
    else:
        # Other
        return -1

def test():
    tests_path = 'testing_area/area_tests/'
    results_path = 'testing_area/area_test_results/'
    expected_path = 'testing_area/area_test_expected/'

    for p in Path(tests_path).glob('**/*.txt'):
        filename = f"{p.name}"
        file = open(filename, 'r')
        lines = file.readlines()
        split_line = lines[0].replace("(", "").replace(")", "").split(" ", 3)
        p1_split = split_line[0].split(",", 1)
        p2_split = split_line[1].split(",", 1)
        p3_split = split_line[2].split(",", 1)
        p4_split = split_line[3].split(",", 1)
        p1 = Point(int(p1_split[0]), int(p1_split[1]))
        p2 = Point(int(p2_split[0]), int(p2_split[1]))
        p3 = Point(int(p3_split[0]), int(p3_split[1]))
        p4 = Point(int(p4_split[0]), int(p4_split[1]))
        result = shape(p1, p2, p3, p4)

        text_file = open(results_path + filename, 'w')
        my_string = 'type your string here'
        text_file.write(result)
        text_file.close()

        return 

if __name__ == "__main__":
    class Point:
        # Structure of a point in 2D space
        def __init__(self, x, y):
            self.x = x
            self.y = y

    while(1):
        mode = input("type 'test', 'user', or 'done': ")

        if (mode == "test"):
            print("test mode begin")
            test()
            # sort_points = sorted_points([Point(-5, -2), Point(-2, -3), Point(-1, 2), Point(0, -1)])
            # for i in range(0, len(sort_points)):
            #     print(sort_points[i].x, sort_points[i].y)
            print("exiting test mode")

        elif (mode == "user"):

            print("user mode begin")
            file_name_usr = input("type file name: ")

            if (exists(file_name_usr)):

                print("user mode finished")
            else:
                print("file does not exist")
            
            print("exiting user mode")

        elif (mode == "done"):
            print("exiting program")
            break

        else:
            print("invalid mode")


# def area(p1, p2, p3, p4):
#     d1 = distSq(p1, p2)
#     d2 = distSq(p2, p3)
#     d3 = distSq(p3, p4)
#     d4 = distSq(p1, p4)
#     d5 = distSq(p1, p3)
#     d6 = distSq(p2, p4)

#     dist_list = [d1, d2, d3, d4, d5, d6]
    
#     if (val == 0 for val in dist_list):
#         return -1

#     sides_2 = [number for number in dist_list if dist_list.count(number) > 1]
#     two_sides = list(set(sides_2))
#     # Check if two sides are equal and diagonals are equal
#     if len(two_sides) == 3:
#         two_sides.sort()
#         # Rectangle: All interior angles are 90 degrees
#         return two_sides[0] * two_sides[1]
#     # elif len(two_sides) == 2:
#     #     # Rhombus
#     #     diag = set(dist_list) - two_sides[0] - two_sides[1]
#     #     return (diag[0]*diag[1])/2

#     sides_4 = [number for number in dist_list if dist_list.count(number) > 3]
#     four_sides = list(set(sides_4))
#     # Check if all sides are equal
#     if (len(four_sides) == 1):
#         diag = set(dist_list) - four_sides[0]
#         if (diag[0] == diag[1]):
#             # Square: All interior angles are 90 degrees, All sides are equal
#             return four_sides[0]*four_sides[0];
#         else:
#             # Rhombus: Two pairs of parallel sides, All sides are equal
#             return (diag[0]*diag[1])/2

#     # Trapezoid: One pair of parallel sides
#     # Parallelogram: Two pairs of parallel sides
#     # Kite
#     # Other