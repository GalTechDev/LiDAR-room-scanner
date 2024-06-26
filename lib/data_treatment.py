import plotly.graph_objects as plt
import numpy as np

def data2plot(h, v, d):
    x = d*np.cos(np.deg2rad(h))*np.cos(np.deg2rad(v))
    y = d*np.sin(np.deg2rad(h))*np.cos(np.deg2rad(v))
    z = d*np.sin(np.deg2rad(v))

    return (x, y, z)

def data2mesh(data_x, data_y, data_z, min_h, max_h, min_v, max_v, res):
    mesh_x = [] #[[], [], ] list of list of vertical data
    mesh_y = []
    mesh_z = []
    
    coef = (max_v-min_v+res)//res

    for hi in range(0, (max_h-min_h)//res):
        mesh_x.append(data_x[hi*coef:(hi+1)*coef])
        mesh_y.append(data_y[hi*coef:(hi+1)*coef])
        mesh_z.append(data_z[hi*coef:(hi+1)*coef])
    
    triangles = [] #[((x1, y1, z1), (x2, y2, z2), (x3, y3, z3)), ...] liste of tuple with 3 points that make shape
    for hi in range(0, (max_h-min_h)//res-1):
        for vi in range(0, (max_v-min_v)//res-1):
            triangles.append(
                (
                    (mesh_x[hi][vi], mesh_y[hi][vi], mesh_z[hi][vi]), 
                    (mesh_x[hi+1][vi], mesh_y[hi+1][vi], mesh_z[hi+1][vi]), 
                    (mesh_x[hi][vi+1], mesh_y[hi][vi+1], mesh_z[hi][vi+1])
                ))
            
            """if hi == 0:
                triangles.append(
                (
                    (mesh_x[hi][vi], mesh_y[hi][vi], mesh_z[hi][vi]), 
                    (mesh_x[hi-1][vi], mesh_y[hi-1][vi], mesh_z[hi-1][vi]), 
                    (mesh_x[hi-1][vi+1], mesh_y[hi-1][vi+1], mesh_z[hi-1][vi+1])
                ))"""
            
    for hi in range(0, (max_h-min_h)//res):
        for vi in range(1, (max_v-min_v)//res):
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