import math

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

def slope(p, q):
    return (q.y - p.y) / (q.x - p.x)

####################################################

################ Shape Areas #######################
def square(side):
    return side ** 2

def rectangle(width, height):
    return width * height

def parallelogram(side, height):
    return side * height

def trapezium(height, width_1, width_2):
    return 0.5 * height * ( width_1 + width_2 )

def rhombus(height, width):
    return 0.5 * height * width

def kite(height, width):
    return 0.5 * height * width

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

    d5 = distSq(p1, p3)
    d6 = distSq(p2, p4)

    dist_list = [d1, d2, d3, d4, d5, d6]

    # any invalid distances, return -1
    if (val == 0 for val in dist_list):
        return -1

    # count the duplicate distances
    sides = [number for number in dist_list if dist_list.count(number) > 1]

    
    # Rectangle: All interior angles are 90 degrees
    # Square: All interior angles are 90 degrees, All sides are equal
    
    # Trapezoid: One pair of parallel sides
    # Rhombus: Two pairs of parallel sides, All sides are equal
    # Parallelogram: Two pairs of parallel sides

    # Kite: Two equal sides, pair must be adjacent and distinct
    # Other



def test():

    pass

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
            # test()
            sort_points = sorted_points([Point(-5, -2), Point(-2, -3), Point(-1, 2), Point(0, -1)])
            for i in range(0, len(sort_points)):
                print(sort_points[i].x, sort_points[i].y)
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