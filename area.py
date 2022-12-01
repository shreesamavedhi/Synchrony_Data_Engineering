import math
import filecmp
from os.path import exists
from pathlib import Path
import pandas as pd
import re

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
    if dx == 0:
        return 0
    return dy/dx

# Function to calculate height of the trapezoid
def findHeight(p1, p2, b, c):
    temp_u = (b - c)**2 + p1**2 - p2**2
    temp_b = 2 * (b - c)
    temp = temp_u / temp_b
    height = math.sqrt(p1 ** 2 - temp **2)
    return height

def remove_tail_dot_zeros(a):
    tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
    return tail_dot_rgx.sub(r'\2',a)

# Source: https://stackoverflow.com/questions/44111169/remove-trailing-zeros-after-the-decimal-point-in-python
####################################################

################ Shape Areas #######################
def square(side):
    return "Square " + str(round(side ** 2, 3))

def rectangle(width, height):
    return "Rectangle " + str(round(width * height, 3))

def parallelogram(side1, side2, angle):
    temp_area = round(side1 * side2 * math.sin(math.radians(angle)), 3)
    return "Parallelogram " + str(temp_area)


def trapezoid(height, width_1, width_2):
    return "Trapezoid " + str(round(0.5 * height * ( width_1 + width_2 ), 3))

def rhombus(height, width):
    return "Rhombus " + str(round(0.5 * height * width, 3))

def kite(height, width):
    return "Kite " + str(round(0.5 * height * width, 3))

####################################################

def shape(p1, p2, p3, p4):

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
    for i in side_list:
        if i == 0:
            # print(side_list)
            print("Other: Invalid side length")
            return -1
    
    for i in angle_list:
        if i >= 180:
            # print(angle_list)
            print("Other: Invalid angle")
            return -1

    if (a1 == a2 == a3 == a4 == 90):
        if(s1 == s2 == s3 == s4):
            # Square: All interior angles are 90 degrees, All sides are equal
            return square(s1)
        else:
            # Rectangle: All interior angles are 90 degrees
            return rectangle(s1, s2)
    
    elif (e1 == e3 and e2 == e4):
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
        print("Other: Other Quadrilateral")
        return -1

def test():
    tests_path = 'testing_area/area_tests/'
    results_path = 'testing_area/area_test_results/'
    expected_path = 'testing_area/area_test_expected/'
    test_flag = True

    for p in Path(tests_path).iterdir():
        filename = f"{p.name}"
        file_ = open(tests_path + filename, 'r')
        lines = file_.readlines()
        split_line = lines[0].replace("(", "").replace(")", "").split(" ", 3)
        p1_split = split_line[0].split(",", 1)
        p2_split = split_line[1].split(",", 1)
        p3_split = split_line[2].split(",", 1)
        p4_split = split_line[3].split(",", 1)
        p1 = Point(int(p1_split[0]), int(p1_split[1]))
        p2 = Point(int(p2_split[0]), int(p2_split[1]))
        p3 = Point(int(p3_split[0]), int(p3_split[1]))
        p4 = Point(int(p4_split[0]), int(p4_split[1]))
        points_temp = [p1, p2, p3, p4]
        points_sorted = sorted_points(points_temp)

        result = shape(points_sorted[0], points_sorted[1], points_sorted[2], points_sorted[3])
        
        if(result != -1):
            result = remove_tail_dot_zeros(result)
            text_file = open(results_path + filename, 'w')
            text_file.write(result)
            text_file.close()
        else:
            text_file = open(results_path + filename, 'w')
            text_file.write("-1")
            text_file.close()
        try:
            # Assertions for each file tested
            assert filecmp.cmp(expected_path + filename, results_path + filename)
        except:
            print(f"test for " + filename + " has unexpected result")
            test_flag = False
            continue

    if(test_flag):
        print("\n $$$ All tests passed!! $$$ \n")
    else:
        print("\n ### Some tests failed ### \n")
        
    return 

if __name__ == "__main__":
    class Point:
        # Structure of a point in 2D space
        def __init__(self, x, y):
            self.x = x
            self.y = y

    print("\n*** Wecome to the Quadrilateral Area Calculator! ***\n \n\
Please enter the coordinates of the four points of your quadrilateral in the following format into a text file: \n\
(x1, y1) (x2, y2) (x3, y3) (x4, y4) \n\
Then, select 'user' mode, and enter the name of the file. \n\
If you would like to test the program, select 'test' mode. \n\
If you would like to exit, select 'done' mode. \n\
")

    while(1):        
        mode = input("Type 'test', 'user', or 'done': ")

        if (mode == "test"):
            print("\n ***test mode begin*** \n")
            test()
            print("***exiting test mode*** \n \n")

        elif (mode == "user"):
            print("\n ***user mode begin*** \n")
            file_name_usr = input("type file name: ")

            if (exists(file_name_usr)):
                file_ = open(file_name_usr, 'r')
                lines = file_.readlines()
                split_line = lines[0].replace("(", "").replace(")", "").split(" ", 3)
                p1_split = split_line[0].split(",", 1)
                p2_split = split_line[1].split(",", 1)
                p3_split = split_line[2].split(",", 1)
                p4_split = split_line[3].split(",", 1)
                p1 = Point(int(p1_split[0]), int(p1_split[1]))
                p2 = Point(int(p2_split[0]), int(p2_split[1]))
                p3 = Point(int(p3_split[0]), int(p3_split[1]))
                p4 = Point(int(p4_split[0]), int(p4_split[1]))
                points_temp = [p1, p2, p3, p4]
                points_sorted = sorted_points(points_temp)

                result = shape(points_sorted[0], points_sorted[1], points_sorted[2], points_sorted[3])

                if(result != -1):
                    result = remove_tail_dot_zeros(result)
                    text_file = open("area_usr_results/" + file_name_usr, 'w')
                    text_file.write(result)
                    text_file.close()
                else:
                    text_file = open("area_usr_results/" + file_name_usr, 'w')
                    text_file.write("-1")
                    text_file.close()

                print("\n file saved! \n")
            else:
                print("\n file does not exist! \n")
            
            print("***exiting user mode*** \n")

        elif (mode == "done"):
            print("\n ***exiting program*** \n")
            break

        else:
            print("\ninvalid mode!\n")