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

def data2mesh(data_x, data_y, data_z):
    mesh_x = [] #[[], [], ] list of list of vertical data
    mesh_y = []
    mesh_z = []
    
    coef = 90//res

    for hi in range(0, 360//res):
        mesh_x.append(data_x[hi*coef:(hi+1)*coef])
        mesh_y.append(data_y[hi*coef:(hi+1)*coef])
        mesh_z.append(data_z[hi*coef:(hi+1)*coef])
    
    triangles = [] #[((x1, y1, z1), (x2, y2, z2), (x3, y3, z3)), ...] liste of tuple with 3 points that make shape
    for hi in range(0, 360//res-1):
        for vi in range(0, 90//res-1):
            triangles.append(
                (
                    (mesh_x[hi][vi], mesh_y[hi][vi], mesh_z[hi][vi]), 
                    (mesh_x[hi+1][vi], mesh_y[hi+1][vi], mesh_z[hi+1][vi]), 
                    (mesh_x[hi][vi+1], mesh_y[hi][vi+1], mesh_z[hi][vi+1])
                ))
            
            if hi == 0:
                triangles.append(
                (
                    (mesh_x[hi][vi], mesh_y[hi][vi], mesh_z[hi][vi]), 
                    (mesh_x[hi-1][vi], mesh_y[hi-1][vi], mesh_z[hi-1][vi]), 
                    (mesh_x[hi-1][vi+1], mesh_y[hi-1][vi+1], mesh_z[hi-1][vi+1])
                ))
            
    for hi in range(0, 360//res):
        for vi in range(1, 90//res):
            triangles.append(
                (
                    (mesh_x[hi][vi], mesh_y[hi][vi], mesh_z[hi][vi]), 
                    (mesh_x[hi-1][vi], mesh_y[hi-1][vi], mesh_z[hi-1][vi]), 
                    (mesh_x[hi][vi-1], mesh_y[hi][vi-1], mesh_z[hi][vi-1])
                ))

    mesh_x.clear()
    mesh_y.clear()
    mesh_z.clear()

    for triangle in triangles:
        mesh_x += [triangle[0][0], triangle[1][0], triangle[2][0]]
        mesh_y += [triangle[0][1], triangle[1][1], triangle[2][1]]
        mesh_z += [triangle[0][2], triangle[1][2], triangle[2][2]]

    return mesh_x, mesh_y, mesh_z

data_x = []
data_y = []
data_z = []

for h, v, d in gen_test_data():
    x, y, z = data2plot(h, v, d)
    data_x.append(x)
    data_y.append(y)
    data_z.append(z)

mesh_x, mesh_y, mesh_z = data2mesh(data_x, data_y, data_z)

m3d = plt.Mesh3d(x=mesh_x, y=mesh_y, z=mesh_z, i=list(range(0, len(mesh_x), 3)), j=list(range(1, len(mesh_x), 3)), k=list(range(2, len(mesh_x), 3)))
m = plt.Scatter3d(x=data_x, y=data_y, z=data_z)
fig = plt.Figure(data=[m])
fig.show()