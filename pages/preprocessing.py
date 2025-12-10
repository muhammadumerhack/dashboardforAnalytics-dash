# pages/preprocessing.py
from dash import html, dcc, dash_table

def layout():
    return html.Div(
        className="container",
        style={"padding": "40px 10px"},
        children=[
            html.H2("Data Preprocessing Pipeline"),
            html.Div(id="preprocess-summary"),
            html.Br(),
            dcc.Tabs(
                id="preprocess-tabs",
                value="tab-missing",
                children=[
                    dcc.Tab(
                        label="1. Missing Values",
                        value="tab-missing",
                        children=[
                            html.Br(),
                            html.H4("Missing Values Analysis"),
                            dash_table.DataTable(
                                id="missing-table",
                                style_table={"maxHeight": "250px", "overflowY": "auto"},
                                style_cell={"textAlign": "left"},
                            ),
                            html.Br(),
                            html.H5("Handle Missing Values"),
                            html.Div(
                                style={"display": "flex", "gap": "10px"},
                                children=[
                                    html.Div(
                                        [
                                            html.Label("Select Column"),
                                            dcc.Dropdown(id="missing-column"),
                                        ],
                                        style={"width": "30%"},
                                    ),
                                    html.Div(
                                        [
                                            html.Label("Method"),
                                            dcc.Dropdown(
                                                id="missing-method",
                                                options=[
                                                    {"label": "Drop rows", "value": "drop"},
                                                    {"label": "Mean (numeric)", "value": "mean"},
                                                    {"label": "Median (numeric)", "value": "median"},
                                                    {"label": "Mode", "value": "mode"},
                                                    {"label": "Constant value", "value": "constant"},
                                                ],
                                            ),
                                        ],
                                        style={"width": "30%"},
                                    ),
                                    html.Div(
                                        [
                                            html.Label("Custom value (optional)"),
                                            dcc.Input(
                                                id="missing-constant",
                                                type="text",
                                                placeholder="Enter value",
                                                style={"width": "100%"},
                                            ),
                                        ],
                                        style={"width": "30%"},
                                    ),
                                ],
                            ),
                            html.Br(),
                            html.Button(
                                "Apply Missing Value Treatment",
                                id="btn-apply-missing",
                                className="btn btn-primary",
                            ),
                            html.Br(),
                            html.Br(),
                            html.Div(id="missing-message"),
                        ],
                    ),
                    dcc.Tab(
                        label="2. Data Types",
                        value="tab-dtypes",
                        children=[
                            html.Br(),
                            html.H4("Current Data Types"),
                            dash_table.DataTable(
                                id="dtype-table",
                                style_cell={"textAlign": "left"},
                            ),
                            html.Br(),
                            html.H5("Change Column Data Type"),
                            html.Div(
                                style={"display": "flex", "gap": "10px"},
                                children=[
                                    html.Div(
                                        [
                                            html.Label("Column"),
                                            dcc.Dropdown(id="dtype-column"),
                                        ],
                                        style={"width": "40%"},
                                    ),
                                    html.Div(
                                        [
                                            html.Label("New Type"),
                                            dcc.Dropdown(
                                                id="dtype-newtype",
                                                options=[
                                                    {"label": "Integer", "value": "int"},
                                                    {"label": "Float", "value": "float"},
                                                    {"label": "Category", "value": "category"},
                                                    {"label": "Datetime", "value": "datetime"},
                                                    {"label": "String", "value": "string"},
                                                ],
                                            ),
                                        ],
                                        style={"width": "40%"},
                                    ),
                                ],
                            ),
                            html.Br(),
                            html.Button(
                                "Apply Type Change",
                                id="btn-apply-dtype",
                                className="btn btn-primary",
                            ),
                            html.Br(),
                            html.Br(),
                            html.Div(id="dtype-message"),
                        ],
                    ),
                    dcc.Tab(
                        label="3. Discretization",
                        value="tab-discretization",
                        children=[
                            html.Br(),
                            html.H4("Discretize Numeric Column"),
                            html.Div(
                                style={"display": "flex", "gap": "10px"},
                                children=[
                                    html.Div(
                                        [
                                            html.Label("Numeric Column"),
                                            dcc.Dropdown(id="disc-column"),
                                        ],
                                        style={"width": "40%"},
                                    ),
                                    html.Div(
                                        [
                                            html.Label("Number of Bins"),
                                            dcc.Input(
                                                id="disc-bins",
                                                type="number",
                                                value=4,
                                                min=2,
                                                max=20,
                                            ),
                                        ],
                                        style={"width": "20%"},
                                    ),
                                ],
                            ),
                            html.Br(),
                            html.Button(
                                "Apply Discretization",
                                id="btn-apply-disc",
                                className="btn btn-primary",
                            ),
                            html.Br(),
                            html.Br(),
                            html.Div(id="disc-message"),
                        ],
                    ),
                    dcc.Tab(
                        label="4. Normalization",
                        value="tab-normalization",
                        children=[
                            html.Br(),
                            html.H4("Normalize Numeric Columns (Min-Max)"),
                            html.Label("Select Columns"),
                            dcc.Dropdown(
                                id="norm-columns",
                                multi=True,
                            ),
                            html.Br(),
                            html.Button(
                                "Apply Normalization",
                                id="btn-apply-norm",
                                className="btn btn-primary",
                            ),
                            html.Br(),
                            html.Br(),
                            html.Div(id="norm-message"),
                        ],
                    ),
                    dcc.Tab(
                        label="5. Encoding",
                        value="tab-encoding",
                        children=[
                            html.Br(),
                            html.H4("Encode Categorical Columns"),
                            html.Label("Select Columns"),
                            dcc.Dropdown(
                                id="enc-columns",
                                multi=True,
                            ),
                            html.Br(),
                            html.Label("Encoding Method"),
                            dcc.Dropdown(
                                id="enc-method",
                                options=[
                                    {"label": "One-Hot Encoding", "value": "onehot"},
                                    {"label": "Label Encoding", "value": "label"},
                                ],
                            ),
                            html.Br(),
                            html.Button(
                                "Apply Encoding",
                                id="btn-apply-enc",
                                className="btn btn-primary",
                            ),
                            html.Br(),
                            html.Br(),
                            html.Div(id="enc-message"),
                        ],
                    ),
                    dcc.Tab(
                        label="6. Train-Test Split",
                        value="tab-split",
                        children=[
                            html.Br(),
                            html.H4("Train-Test Split"),
                            html.Label("Target Column"),
                            dcc.Dropdown(id="split-target"),
                            html.Br(),
                            html.Label("Train Size (between 0 and 1)"),
                            dcc.Slider(
                                id="split-train-size",
                                min=0.5,
                                max=0.9,
                                step=0.05,
                                value=0.7,
                                marks={0.6: "0.6", 0.7: "0.7", 0.8: "0.8"},
                            ),
                            html.Br(),
                            html.Button(
                                "Run Train-Test Split",
                                id="btn-apply-split",
                                className="btn btn-primary",
                            ),
                            html.Br(),
                            html.Br(),
                            html.Pre(id="split-message"),
                        ],
                    ),
                ],
            ),
            html.Hr(),
            html.Button(
                "Download Processed Dataset",
                id="btn-download-processed",
                className="btn btn-success",
            ),
            dcc.Download(id="download-processed"),
        ],
    )
