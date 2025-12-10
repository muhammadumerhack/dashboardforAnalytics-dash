# pages/bivariate.py
from dash import html, dcc

def layout():
    return html.Div(
        className="container",
        style={"padding": "40px 10px"},
        children=[
            html.H2("Bivariate Analysis"),
            html.Div(
                style={"display": "flex", "gap": "20px"},
                children=[
                    html.Div(
                        style={"width": "25%"},
                        children=[
                            html.Label("X-axis Variable"),
                            dcc.Dropdown(id="bi-x", placeholder="Select X variable"),
                            html.Br(),
                            html.Label("Y-axis Variable"),
                            dcc.Dropdown(id="bi-y", placeholder="Select Y variable"),
                            html.Br(),
                            html.Label("Select Analysis Type"),
                            dcc.Dropdown(
                                id="bi-plot-type",
                                options=[
                                    {"label": "Scatter Plot", "value": "scatter"},
                                    {"label": "Box Plot", "value": "box"},
                                    {"label": "Violin Plot", "value": "violin"},
                                    {"label": "Bar Plot", "value": "bar"},
                                ],
                                value="scatter",
                            ),
                        ],
                    ),
                    html.Div(
                        style={"width": "70%"},
                        children=[
                            html.H4("Correlation / Interpretation"),
                            html.Div(id="bi-summary"),
                            html.Br(),
                            dcc.Graph(id="bi-graph",style={"height": "500px"},clear_on_unhover=True),
                        ],
                    ),
                ],
            ),
        ],
    )
