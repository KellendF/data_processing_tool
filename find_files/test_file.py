'''

'''
import numpy as np

import mahotas.polygon

img_size = (10,10)
part_point = [[1,1],[3,1],[6,3],[7,3],[7,6],[8,2],[9,1]]
damage_point = [[4,1],[4,6],[3,8],[5,8],[2,6]]

img_arr = np.zeros(img_size)
part_point_tuple = [tuple(point) for point in part_point]
mahotas.polygon.fill_polygon(part_point_tuple, img_arr, color=1)
list = np.argwhere(img_arr==1)
print(list)
# for damage in damage_point:
#     mahotas.polygon.fill_polygon(damage, img_arr, color=2)
# damage_point_tuple = [tuple(point) for point in damage_point]
# mahotas.polygon.fill_polygon(damage_point_tuple, img_arr, color=2)

# print(img_arr)