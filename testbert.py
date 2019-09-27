#https://medium.com/@manivannan_data/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd

import numpy as np

# points
# v0 = np.array([1, 1])
# v1 = np.array([4, 2])
# v2 = np.array([5, 2])
# v3 = np.array([6, 4])
# v4 = np.array([4, 4])
# v5 = np.array([3, 6])
# v6 = np.array([1, 5])
# v7 = np.array([2, 3])

v0 = np.array([1, 1])
v1 = np.array([1, 4])
v2 = np.array([4, 4])
v3 = np.array([4, 1])
v4 = np.array([2, 2])
v5 = np.array([2, 3])
v6 = np.array([3, 3])
v7 = np.array([3, 2])

points = [
    v0,
    v1,
    v2,
    v3,
    v4,
    v5,
    v6,
    v7
]

center = np.mean(points, axis=0)
center_y_zero = np.array([center[0], 0])


def angle_between_points(a, b, c):
    """:return angle in degree between points a, b, c"""
    # if a[0] >= b[0]:
    #     a, b = b, a

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    degrees = np.degrees(angle)

    if a[0] >= b[0]:
        degrees = 360 - degrees

    return degrees


print(f"v0 {angle_between_points(v0, center, center_y_zero)}")
print(f"v1 {angle_between_points(v1, center, center_y_zero)}")
print(f"v2 {angle_between_points(v2, center, center_y_zero)}")
print(f"v3 {angle_between_points(v3, center, center_y_zero)}")
print(f"v4 {angle_between_points(v4, center, center_y_zero)}")
print(f"v5 {angle_between_points(v5, center, center_y_zero)}")
print(f"v6 {angle_between_points(v6, center, center_y_zero)}")
print(f"v7 {angle_between_points(v7, center, center_y_zero)}")

