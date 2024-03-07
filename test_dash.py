from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objects as plt
import test

MAX_RES = 10
MIN_VERCICAL = -45

def get_Div_parameters(resolution):
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

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children="LiDAR 3D view test", style={"textAlign":"center"}),
    html.Div(get_Div_parameters(1), id="div-range-slider"),
    html.H3(children="Resolution (step)"),
    dcc.Input(id="res-input", type="number", placeholder="resolution", min=1, max=MAX_RES, step=1, value=1),
    html.Button('Start', id='start-btn'),
    dcc.Graph(id='graph-content',  style={"height" : "630px", "width" : "100%"}),
])

last_data = [0, plt.Figure()]

@callback(
    Output("graph-content", "figure"),
    Input("h-range-slider", "value"),
    Input("v-range-slider", "value"),
    Input("res-input", "value"),
    Input("start-btn", "n_clicks"),
)
def update_graph(h_value, v_value, res, n_click):
    if n_click!=None and n_click!=last_data[0]:
        
        last_data[0]+=1
        last_data[1] = test.test_plotly.get_test_fig("mesh", res=res, min_h=h_value[0], max_h=h_value[1], min_v=v_value[0], max_v=v_value[1])

    return last_data[1]
    
@callback(
    Output("div-range-slider", "children"),
    Input("res-input", "value"),
)
def update_parameters(value):
    return get_Div_parameters(value)

if __name__ == "__main__":
    app.run(debug=True)
