import plotly.graph_objects as plt
import numpy as np

#Visualisation très performente sur de nombreux points
#Interface web

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
            
            if hi == 0:
                triangles.append(
                (
                    (mesh_x[hi][vi], mesh_y[hi][vi], mesh_z[hi][vi]), 
                    (mesh_x[hi-1][vi], mesh_y[hi-1][vi], mesh_z[hi-1][vi]), 
                    (mesh_x[hi-1][vi+1], mesh_y[hi-1][vi+1], mesh_z[hi-1][vi+1])
                ))
            
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


#test
def gen_test_data(min_h, max_h, min_v, max_v, res):
    for h in range(min_h, max_h, res):
        for v in range(min_v, max_v+res, res):
            yield (h,v, 1)

def get_test_data(min_h, max_h, min_v, max_v, res):
    data_x = []
    data_y = []
    data_z = []

    for h, v, d in gen_test_data(min_h, max_h, min_v, max_v, res):
        x, y, z = data2plot(h, v, d)
        data_x.append(x)
        data_y.append(y)
        data_z.append(z)
    return data_x, data_y, data_z

def get_test_fig(fig_type, res, min_h, max_h, min_v, max_v):
    """
    type : "plot" or "mesh"
    """
    max_v += res

    data_x, data_y, data_z = get_test_data(min_h, max_h, min_v, max_v, res)
    mesh_x, mesh_y, mesh_z = data2mesh(data_x, data_y, data_z, min_h, max_h, min_v, max_v, res)
    get_test_obj(mesh_x, mesh_y, mesh_z)
    m3d = plt.Mesh3d(x=mesh_x, y=mesh_y, z=mesh_z, i=list(range(0, len(mesh_x), 3)), j=list(range(1, len(mesh_x), 3)), k=list(range(2, len(mesh_x), 3)))
    m = plt.Scatter3d(x=data_x, y=data_y, z=data_z)
    if fig_type == "plot":
        data = m
    elif fig_type == "mesh":
        data = m3d
    else:
        raise Exception("fig_type unreconised")
    
    fig = plt.Figure(data=data)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig

def get_test_obj(mesh_x, mesh_y, mesh_z, filename="test.obj"):
    i_list=list(range(1, len(mesh_x)+1, 3))
    j_list=list(range(2, len(mesh_x)+1, 3))
    k_list=list(range(3, len(mesh_x)+1, 3))
    obj = ""
    for x,y,z in list(zip(mesh_x, mesh_y, mesh_z)):
        obj+=f"v  {x} {y} {z}\n"
    for i,j,k in list(zip(i_list, j_list, k_list)):
        pass
        obj+=f"f  {i} {j} {k}\n"
    with open(filename, "w") as f:
        f.write(obj)

    

    

if __name__ == "__main__":
    fig = get_test_fig("mesh", 1,0,360,-45,90)
    #fig.show()
