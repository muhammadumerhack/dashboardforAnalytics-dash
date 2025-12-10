# pages/univariate.py
from dash import html, dcc

def layout():
    return html.Div(
        className="container",
        style={"padding": "40px 10px"},
        children=[
            html.H2("Univariate Analysis"),
            html.Div(
                style={"display": "flex", "gap": "20px"},
                children=[
                    html.Div(
                        style={"width": "25%"},
                        children=[
                            html.Label("Select Variable"),
                            dcc.Dropdown(
                                id="uni-variable",
                                placeholder="Select a column",
                            ),
                            html.Br(),
                            html.Label("Select Analysis Type"),
                            dcc.Dropdown(
                                id="uni-plot-type",
                                options=[
                                    {"label": "Histogram", "value": "hist"},
                                    {"label": "Box Plot", "value": "box"},
                                    {"label": "Violin Plot", "value": "violin"},
                                    {"label": "Count Plot (Categorical)", "value": "count"},
                                    {"label": "Distribution Plot", "value": "dist"},
                                ],
                                value="hist",
                            ),
                        ],
                    ),
                    html.Div(
                        style={"width": "70%"},
                        children=[
                            html.H4("Statistical Summary"),
                            html.Div(id="uni-summary"),
                            html.Br(),
                            dcc.Graph(id="uni-graph",style={"height": "500px"},clear_on_unhover=True),
                        ],
                    ),
                ],
            ),
        ],
    )
