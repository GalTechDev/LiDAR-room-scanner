import plotly.graph_objects as plt
from lib.data_treatment import data2plot, data2mesh
from lib.arduino2python import Arduino

def get_plot(data):

    data_x, data_y, data_z = data
    
    data = plt.Scatter3d(x=data_x, y=data_y, z=data_z)
    
    fig = plt.Figure(data=data)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig

def get_mesh(data, parameter):
    res = parameter["res"]
    min_h = parameter["min_h"]
    max_h = parameter["max_h"]
    min_v = parameter["min_v"]
    max_v = parameter["max_v"]

    data_x, data_y, data_z = data
    mesh_x, mesh_y, mesh_z = data2mesh(data_x, data_y, data_z, min_h, max_h, min_v, max_v, res)
    
    m3d = plt.Mesh3d(x=mesh_x, y=mesh_y, z=mesh_z, i=list(range(0, len(mesh_x), 3)), j=list(range(1, len(mesh_x), 3)), k=list(range(2, len(mesh_x), 3)))
    data = m3d
    
    fig = plt.Figure(data=data)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig