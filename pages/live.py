from dash import register_page, Dash, html, dcc, callback, Output, Input, State
import plotly.graph_objects as plt
import plotly.graph_objects as go
from lib.arduino2python import get_connected_port, Arduino, FakeArduino
from lib.graph import get_mesh, get_plot

MAX_RES = 10
MIN_VERCICAL = -45

arduino: Arduino = FakeArduino()

def get_Div_parameters(resolution):
    if not arduino:
        return []
    max_h = (360//resolution)*resolution

    min_v = -(-MIN_VERCICAL//resolution)*resolution
    max_v = (90//resolution)*resolution
    return [
        html.H3(children="Horisontal scan range"),
        dcc.RangeSlider(0, max_h, resolution, value=[0, max_h], id='h-range-slider', tooltip={"placement": "bottom", "always_visible": True}, marks={
            0: {'label': '0°'},
            90: {'label': '90°'},
            180: {'label': '180°'},
            270: {'label': '270°'},
            360: {'label': '360°'}
        }),

        html.H3(children="Vertical scan range"),
        dcc.RangeSlider(min_v, max_v, resolution, value=[0, max_v], id='v-range-slider', tooltip={"placement": "bottom", "always_visible": True}, marks={
            min_v: {'label': f'{min_v}°'},
            0: {'label': '0°'},
            45: {'label': '45°'},
            max_v: {'label': f'{max_v}°'},
        }),
    ]

layout = html.Div([
    html.H1(children="LiDAR 3D view test", style={"textAlign":"center"}),
    html.Div(children=[
        dcc.Dropdown(options=get_connected_port(), id="dropdown-port"),
    ]),
    html.Div(children=[
        html.Div(children=get_Div_parameters(1), id="div-range-slider"),
        html.H3(children="Resolution (step)"),
        dcc.Input(id="res-input", type="number", placeholder="resolution", min=1, max=MAX_RES, step=1, value=1),
        html.Button("Start", id="start-btn"),
        html.Div(
            dcc.Graph(id="graph-content",  style={"height" : "630px", "width" : "100%"}), 
            style={"display": "none"}, 
            id="div-graph"
        ),
        dcc.Interval(id='interval-component',interval=5*1000, n_intervals=0)
    ], style={"display": "none"}, id="div-parameter")
])
scene = dict(
    camera=dict(
        up=dict(x=0, y=-1, z=0),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=1, y=-1, z=1)
    )
)
fig_layout = go.Layout(scene=scene)
default_figure = plt.Figure(layout=fig_layout)
default_figure['layout']['uirevision'] = 'Do not change'
last_data = [0, default_figure, 1]
port = None

@callback(
    Output("div-graph", "style"),
    State("h-range-slider", "value"),
    State("v-range-slider", "value"),
    State("res-input", "value"),
    Input("start-btn", "n_clicks"),
)
def update_graph(h_value, v_value, res, n_click):  
    if n_click:
        arduino.set_gen_parameter(h_value, v_value, res)
        arduino.start(arduino.gen_parameter["min_h"], arduino.gen_parameter["max_h"], arduino.gen_parameter["min_v"], arduino.gen_parameter["max_v"], arduino.gen_parameter["res"])
        last_data[0]+=1
        last_data[1] = get_plot(arduino.get_data())

    return last_data[1]

@callback(
        Output("graph-content", "figure"),
        Input("interval-component", "n_intervals"),
        State("graph-content", "figure")
)
def update_graph(n, fig):
    if fig == None:
        return last_data[1]
    plot = get_plot(arduino.get_data())
    fig["data"] = plot.data
    return fig
    
@callback(
    Output("div-range-slider", "children"),
    Input("res-input", "value"),
)
def update_parameters(value):
    return get_Div_parameters(value if value!=None else last_data[2])

@callback(
    Output("div-parameter", "style"),
    Input("dropdown-port", "value"),
)
def set_port(value):
    if value != None:
        global arduino
        arduino = Arduino(value)
        return {"display": "block"}
    else:
        return {"display": "none"}

if __name__ == "__main__":
    app = Dash(__name__)
    app.layout = layout
    app.run(debug=True)
else:
    register_page(__name__, path=f'/live')
