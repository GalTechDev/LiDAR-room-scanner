from dash import register_page,Dash, html, dcc, callback, Output, Input

layout = html.Div([
    html.H1(children="LiDAR 3D view test", style={"textAlign":"center"}),
])

if __name__ == "__main__":
    app = Dash(__name__)
    app.layout = layout
    app.run(debug=True)
else:
    register_page(__name__, path=f'/')