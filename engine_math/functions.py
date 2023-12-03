from pygame import Vector2 as vec2
import math

def get_normal_of_segment(start:vec2, end:vec2) -> vec2:
    dx = end.x - start.x
    dy = end.y - start.y
    if dx == 0 and dy == 0:
        return vec2(0, 0)
    vec = vec2(-dy, dx)
    return vec.normalize() * -1


# ClockWise sort
def get_angle(point:vec2, center:vec2) -> float:
    x = point[0] - center[0]
    y = point[1] - center[1]
    angle = math.atan2(y, x)
    if angle <= 0:
        angle += math.pi * 2
    return angle

def compare_point(center:vec2, point1:vec2, point2:vec2) -> bool:
    angle1 = get_angle(center, point1)
    angle2 = get_angle(center, point2)
    if angle1 < angle2:
        return True
    if (angle1 == angle2) and \
        (point1.length_squared() < point2.length_squared):
        return True
    return False

def sort_points(points:list[vec2], center:vec2):
    end = len(points)
    if end <= 1:
        return
    i = 1
    while i < end:
        if not compare_point(center, points[i - 1], points[i]):
            points[i - 1], points[i] = points[i], points[i - 1]
            i = 1
        else:
            i += 1

def clockwise_sort(points:list[vec2]):
    center = vec2(0, 0)
    for point in points:
        center += point
    center /= len(points)
    for point in points:
        point -= center
    sort_points(points, center)
    for point in points:
        point += center

