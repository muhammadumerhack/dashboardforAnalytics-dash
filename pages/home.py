# pages/home.py
from dash import html, dcc

def layout():
    return html.Div(
        className="container",
        style={"padding": "40px 10px"},
        children=[
            html.H2("Welcome to Data Science Dashboard"),
            html.H4("Business Use Case"),
            html.P(
                "This dashboard helps us explore the dataset, perform univariate "
                "and bivariate analysis, and run a full preprocessing pipeline."
            ),
            html.Ul(
                [
                    html.Li("Upload CSV datasets or use the default ecommerce data."),
                    html.Li("View univariate distributions and summaries."),
                    html.Li("Explore relationships between two variables."),
                    html.Li("Run a step-by-step preprocessing pipeline and download the result."),
                ]
            ),
            html.Hr(),
            html.H4("Upload Your Dataset"),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    "Drag and Drop or Select a CSV File",
                    style={
                        "padding": "40px",
                        "border": "2px dashed #999",
                        "textAlign": "center",
                    },
                ),
                multiple=False,
            ),
            html.Br(),
            html.Div(id="upload-status"),
            html.Br(),
            html.P(
                "If no file is uploaded, the dashboard uses our default ecommerce dataset."
            ),
        ],
    )
