import json
from map import bricks_xy

bricks = []
for xy in bricks_xy:
    bricks.append(xy)
    print(xy)
d_b = {"bricks": bricks}


with open('map/armors.txt', "a") as file:
    json.dump(d_b, file)




