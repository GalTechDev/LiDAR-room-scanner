import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import numpy as np

#Visualisation peu performente sur de nombreux points

res = 5
d = 1

def gen_test_data():
    for h in range(0, 360, res):
        for v in range(0, 90, res):
            yield (h,v,d)

def data2plot(h, v, d):
    x = d*np.cos(np.deg2rad(h))
    y = d*np.sin(np.deg2rad(h))
    z = d*np.sin(np.deg2rad(v))

    return ([x], [y], [z])


axes = [5, 5, 5]
data = np.ones(axes)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.axis('on')

for h, v, d in gen_test_data():
    data = data2plot(h, v, d)
    print(data)
    ax.scatter(*data, marker="o")

plt.show()