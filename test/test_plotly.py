import plotly.graph_objects as plt
import numpy as np

#Visualisation très performente sur de nombreux points
#Interface web

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

    return (x, y, z)

data_x = []
data_y = []
data_z = []

for h, v, d in gen_test_data():
    x, y, z = data2plot(h, v, d)
    data_x.append(x)
    data_y.append(y)
    data_z.append(z)

m = plt.Scatter3d(x=data_x, y=data_y, z=data_z)
fig = plt.Figure(data=m)
fig.show()