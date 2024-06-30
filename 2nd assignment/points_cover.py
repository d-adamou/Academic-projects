import argparse
from itertools import combinations


def read_points(file):
    p = set()
    with open(file) as r:
        for line in r:
            # Split lines to integers
            points = [int(x) for x in line.split()]
            if len(points) != 2:
                continue
            p.add((points[0], points[1]))
    return p


# find the line between two points.
def find_lines(point1, point2):
    if (point1[0] == point2[0]):
        line = (point1[0])
    else:
        a = (point1[1] - point2[1]) / (point1[0] - point2[0])
        b = point1[1] - (point1[0] * a)
        line = (a, b)
    return line


# find parallel lines between two points.
def find_parallel_lines(point1, point2):
    line = None
    if (point1[0] == point2[0]):
        line = (point1[0], 0)
    elif (point1[1] == point2[1]):
        line = (0, point1[1])
    return line


# if b = 1, it's parallels.
def find_all_lines(points, b):
    all_lines = {}
    # find all the possible lines without the doubles and themselves.
    for p in range(len(points) - 1):
        for q in range(p + 1, len(points)):
            if b == 0:
                line = find_lines(points[p], points[q])
            else:
                line = find_parallel_lines(points[p], points[q])
            if line:
                if line not in all_lines.keys():
                    all_lines[line] = {
                        points[p], points[q]}
                else:
                    # don't check because sets don't keep dublicates.
                    all_lines[line].add(points[p])
                    all_lines[line].add(points[q])
    # for points who don't have another point in their parallel.
    if b == 1:
        for p in points:
            if ((p[0], 0) not in all_lines.keys()) and ((0, p[1]) not in all_lines.keys()):
                all_lines[(0, p[1])] = {p, (p[0] + 1, p[1])}
    return all_lines


# for printing in appropriate form.
def print_points(list):
    list1 = []
    for s in list:
        list1.append(sorted(s))
    list1.sort(key=lambda x: x[0])
    list2 = (sorted(list1, key=len, reverse=True))
    for l in list2:
        for k in l:
            print(k, end=" ")
        print()


def full_solution(file, b):
    points_set = read_points(file)
    points = list(points_set)
    all_lines = find_all_lines(points, b)
    for r in (range(len(points))):
        for i in combinations(all_lines.values(), r):
            # make tuples into set.
            subset = set()
            for t in i:
                subset.update(t)
            # if it is a superset it means it contains all the points.
            if subset.issuperset(points_set):
                l = []
                for t in i:
                    l.append(t)
                print_points(l)
                break
        if subset.issuperset(points_set):
            break


def greedy_solution(file, b):
    points_set = read_points(file)
    points = list(points_set)
    all_lines = find_all_lines(points, b)
    values = all_lines.values()
    # make the set into list in order to sort them.
    lines_list = list(values)
    lines_list2 = (sorted(lines_list, key=len, reverse=True))
    subset = set()
    list1 = []
    while (not subset.issuperset(points_set)):
        # find every time the set with the most points uncovered.
        max = 0
        max_set = None
        for l in lines_list2:
            count = 0
            for s in l:
                if s not in subset:
                    count = count + 1
            if count > max:
                max = count
                max_set = l
        lines_list2.remove(max_set)
        subset.update(max_set)
        list1.append(max_set)
    print_points(list1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Set covering: full/greedy/parallel")

    parser.add_argument("-f", "--full",
                        help="run the full solution", action='store_true', default=False)
    parser.add_argument("-g", "--grammic",
                        help="only vertically or horizontally lines", action='store_true', default=False)
    parser.add_argument("points_file", help="name of points file")

    args = parser.parse_args()

    if (args.full) and (args.grammic):
        full_solution(args.points_file, 1)
    elif (args.full):
        full_solution(args.points_file, 0)
    elif (args.grammic):
        greedy_solution(args.points_file, 1)
    else:
        greedy_solution(args.points_file, 0)
