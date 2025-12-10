# app.py
import base64
import io

import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
from sklearn.model_selection import train_test_split

from pages.home import layout as home_layout
from pages.univariate import layout as univariate_layout
from pages.bivariate import layout as bivariate_layout
from pages.preprocessing import layout as preprocessing_layout

# -------------------------------------------------------------------
# Paths to your default data (change file names if needed)
# -------------------------------------------------------------------
RAW_DATA_PATH = "data/raw_data.csv"              # raw csv
EDA_DATA_PATH = "data/preprocessed_data.csv"     # cleaned csv

def load_default_data():
    raw_df = pd.read_csv(RAW_DATA_PATH)
    eda_df = pd.read_csv(EDA_DATA_PATH)
    return raw_df, eda_df

raw_default, eda_default = load_default_data()

def df_to_store(df: pd.DataFrame) -> dict:
    return df.to_json(date_format="iso", orient="split")

def store_to_df(data):
    if data is None:
        return pd.DataFrame()

    if isinstance(data, bytes):
        data = data.decode("utf-8")

    if isinstance(data, dict):
        return pd.read_json(data, orient="split")

    return pd.read_json(io.StringIO(data), orient="split")

# -------------------------------------------------------------------
# App + basic layout
# -------------------------------------------------------------------
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Top navigation bar
navbar = dbc.NavbarSimple(
    brand="Data Science Dashboard",
    brand_href="/",
    color="success",
    dark=True,
    children=[
        dbc.NavItem(dcc.Link("Home", href="/", className="nav-link")),
        dbc.NavItem(dcc.Link("Univariate Analysis", href="/univariate", className="nav-link")),
        dbc.NavItem(dcc.Link("Bivariate Analysis", href="/bivariate", className="nav-link")),
        dbc.NavItem(dcc.Link("Preprocessing", href="/preprocessing", className="nav-link")),
    ],
)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        navbar,
        # hidden stores to share data across pages
        dcc.Store(id="raw-data-store", data=df_to_store(raw_default)),
        dcc.Store(id="eda-data-store", data=df_to_store(eda_default)),
        html.Div(id="page-content"),
    ]
)

# -------------------------------------------------------------------
# Routing
# -------------------------------------------------------------------
@callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/univariate":
        return univariate_layout()
    elif pathname == "/bivariate":
        return bivariate_layout()
    elif pathname == "/preprocessing":
        return preprocessing_layout()
    # default
    return home_layout()

# -------------------------------------------------------------------
# File upload (Home page) – shared for all pages
# -------------------------------------------------------------------
@callback(
    Output("upload-status", "children"),
    Output("raw-data-store", "data", allow_duplicate=True),
    Output("eda-data-store", "data"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True,
)
def handle_upload(contents, filename):
    if contents is None:
        return no_update, no_update, no_update

    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    except Exception:
        return "Error: could not read the uploaded file as CSV.", no_update, no_update

    msg = f"Uploaded file: {filename} | Shape: {df.shape[0]} rows, {df.shape[1]} columns"

    # For uploaded data, use same DF as both raw and EDA baseline
    return msg, df_to_store(df), df_to_store(df)

# ===================================================================
# UNIVARIATE ANALYSIS CALLBACKS
# ===================================================================
@callback(
    Output("uni-variable", "options"),
    Input("eda-data-store", "data"),
)
def populate_uni_vars(data):
    df = store_to_df(data)
    return [{"label": col, "value": col} for col in df.columns]

@callback(
    Output("uni-summary", "children"),
    Output("uni-graph", "figure"),
    Input("uni-variable", "value"),
    Input("uni-plot-type", "value"),
    Input("eda-data-store", "data"),
)
def update_univariate(var, plot_type, data):
    df = store_to_df(data)
    if var is None:
        empty_fig = px.scatter()
        empty_fig.update_layout(height=450)
        return "Please select a variable.", empty_fig

    series = df[var]

    # summary
    if pd.api.types.is_numeric_dtype(series):
        desc = series.describe().to_frame("Value").reset_index()
    else:
        desc = series.value_counts().to_frame("Count").reset_index().rename(
            columns={"index": "Value"}
        )

    summary_table = dash_table.DataTable(
        data=desc.to_dict("records"),
        columns=[{"name": c, "id": c} for c in desc.columns],
        style_table={"maxHeight": "300px", "overflowY": "auto"},
        style_cell={"textAlign": "left"},
    )

    # graph
    if plot_type == "hist":
        fig = px.histogram(df, x=var, nbins=30)
    elif plot_type == "box":
        fig = px.box(df, x=var)
    elif plot_type == "violin":
        fig = px.violin(df, x=var, box=True)
    elif plot_type == "count":
            vc = df[var].value_counts().reset_index()
            vc.columns = [var, "Count"]  # rename properly
            fig = px.bar(vc, x=var, y="Count")

    else:  # distribution (hist + box style)
        fig = px.histogram(df, x=var, nbins=30)

    fig.update_layout(template="simple_white", height=450)

    return summary_table, fig

# ===================================================================
# BIVARIATE ANALYSIS CALLBACKS
# ===================================================================
@callback(
    Output("bi-x", "options"),
    Output("bi-y", "options"),
    Input("eda-data-store", "data"),
)
def populate_bi_vars(data):
    df = store_to_df(data)
    opts = [{"label": c, "value": c} for c in df.columns]
    return opts, opts

@callback(
    Output("bi-graph", "figure"),
    Output("bi-summary", "children"),
    Input("bi-x", "value"),
    Input("bi-y", "value"),
    Input("bi-plot-type", "value"),
    Input("eda-data-store", "data"),
)
def update_bivariate(x, y, plot_type, data):
    df = store_to_df(data)
    if x is None or y is None:
        empty_fig = px.scatter()
        empty_fig.update_layout(height=450)
        return empty_fig, "Please select both X and Y variables."


    if plot_type == "scatter":
        fig = px.scatter(df, x=x, y=y)
    elif plot_type == "box":
        fig = px.box(df, x=x, y=y)
    elif plot_type == "violin":
        fig = px.violin(df, x=x, y=y, box=True)
    else:  # bar
        fig = px.bar(df, x=x, y=y)

    fig.update_layout(template="simple_white", height=450)

    # simple correlation message for numeric pairs
    msg = ""
    if pd.api.types.is_numeric_dtype(df[x]) and pd.api.types.is_numeric_dtype(df[y]):
        corr = df[[x, y]].corr().iloc[0, 1]
        msg = f"Correlation between {x} and {y}: {corr:.3f}"
    else:
        msg = "Correlation only computed for numeric X and Y."

    return fig, msg

# ===================================================================
# PREPROCESSING PIPELINE CALLBACKS
# ===================================================================

# 1) Update summary + dropdown options whenever raw data changes
@callback(
    Output("preprocess-summary", "children"),
    Output("missing-table", "data"),
    Output("missing-table", "columns"),
    Output("dtype-table", "data"),
    Output("dtype-table", "columns"),
    Output("missing-column", "options"),
    Output("dtype-column", "options"),
    Output("disc-column", "options"),
    Output("norm-columns", "options"),
    Output("enc-columns", "options"),
    Output("split-target", "options"),
    Input("raw-data-store", "data"),
)
def refresh_preprocess_views(data):
    df = store_to_df(data)

    # summary text
    mv_total = df.isna().sum().sum()
    summary = html.Div(
        [
            html.P(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}"),
            html.P(f"Total missing values: {mv_total}"),
        ]
    )

    # missing values table
    mv = df.isna().sum()
    mv_df = mv[mv > 0].to_frame("Missing Count").reset_index()
    mv_df.rename(columns={"index": "Column"}, inplace=True)

    mv_data = mv_df.to_dict("records")
    mv_cols = [{"name": c, "id": c} for c in mv_df.columns]

    # dtype table
    dt_df = pd.DataFrame(
        {"Column": df.columns, "Dtype": df.dtypes.astype(str).values}
    )
    dt_data = dt_df.to_dict("records")
    dt_cols = [{"name": c, "id": c} for c in dt_df.columns]

    # options
    all_cols = [{"label": c, "value": c} for c in df.columns]
    num_cols = [
        {"label": c, "value": c}
        for c in df.select_dtypes(include="number").columns
    ]
    cat_cols = [
        {"label": c, "value": c}
        for c in df.select_dtypes(include="object").columns
    ]

    return (
        summary,
        mv_data,
        mv_cols,
        dt_data,
        dt_cols,
        all_cols,          # missing-column
        all_cols,          # dtype-column
        num_cols,          # disc-column
        num_cols,          # norm-columns
        cat_cols,          # enc-columns
        all_cols,          # split-target
    )

# 2) Missing values
@callback(
    Output("raw-data-store", "data", allow_duplicate=True),
    Output("missing-message", "children"),
    Input("btn-apply-missing", "n_clicks"),
    State("missing-column", "value"),
    State("missing-method", "value"),
    State("missing-constant", "value"),
    State("raw-data-store", "data"),
    prevent_initial_call=True,
)
def apply_missing(n_clicks, column, method, custom_value, data):
    if n_clicks is None or column is None or method is None:
        return no_update, "Select a column and method."

    df = store_to_df(data)

    if method == "drop":
        df = df[df[column].notna()]
        msg = f"Dropped rows where {column} was missing."
    elif method == "mean":
        df[column].fillna(df[column].mean(), inplace=True)
        msg = f"Filled missing {column} with mean."
    elif method == "median":
        df[column].fillna(df[column].median(), inplace=True)
        msg = f"Filled missing {column} with median."
    elif method == "mode":
        df[column].fillna(df[column].mode()[0], inplace=True)
        msg = f"Filled missing {column} with mode."
    else:  # constant
        df[column].fillna(custom_value, inplace=True)
        msg = f"Filled missing {column} with constant value: {custom_value}"

    return df_to_store(df), msg

# 3) Data type conversion
@callback(
    Output("raw-data-store", "data", allow_duplicate=True),
    Output("dtype-message", "children"),
    Input("btn-apply-dtype", "n_clicks"),
    State("dtype-column", "value"),
    State("dtype-newtype", "value"),
    State("raw-data-store", "data"),
    prevent_initial_call=True,
)
def apply_dtype(n_clicks, column, newtype, data):
    if n_clicks is None or column is None or newtype is None:
        return no_update, "Select a column and new data type."

    df = store_to_df(data)

    try:
        if newtype == "int":
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
        elif newtype == "float":
            df[column] = pd.to_numeric(df[column], errors="coerce")
        elif newtype == "category":
            df[column] = df[column].astype("category")
        elif newtype == "datetime":
            df[column] = pd.to_datetime(df[column], errors="coerce")
        else:  # string
            df[column] = df[column].astype(str)
    except Exception:
        return no_update, "Conversion failed, please check the column values."

    return df_to_store(df), f"Converted {column} to {newtype}."

# 4) Discretization
@callback(
    Output("raw-data-store", "data", allow_duplicate=True),
    Output("disc-message", "children"),
    Input("btn-apply-disc", "n_clicks"),
    State("disc-column", "value"),
    State("disc-bins", "value"),
    State("raw-data-store", "data"),
    prevent_initial_call=True,
)
def apply_discretization(n_clicks, column, bins, data):
    if n_clicks is None or column is None or bins is None:
        return no_update, "Select a numeric column and number of bins."

    df = store_to_df(data)
    new_col = f"{column}_bin"
    df[new_col] = pd.cut(df[column], bins=bins, labels=False, include_lowest=True)

    return df_to_store(df), f"Created discretized column {new_col} with {bins} bins."

# 5) Normalization (min-max)
@callback(
    Output("raw-data-store", "data", allow_duplicate=True),
    Output("norm-message", "children"),
    Input("btn-apply-norm", "n_clicks"),
    State("norm-columns", "value"),
    State("raw-data-store", "data"),
    prevent_initial_call=True,
)
def apply_normalization(n_clicks, columns, data):
    if n_clicks is None or not columns:
        return no_update, "Select at least one numeric column to normalize."

    df = store_to_df(data)
    for col in columns:
        col_min = df[col].min()
        col_max = df[col].max()
        if col_max != col_min:
            df[col] = (df[col] - col_min) / (col_max - col_min)

    return df_to_store(df), f"Applied min-max normalization to: {', '.join(columns)}."

# 6) Encoding
@callback(
    Output("raw-data-store", "data", allow_duplicate=True),
    Output("enc-message", "children"),
    Input("btn-apply-enc", "n_clicks"),
    State("enc-columns", "value"),
    State("enc-method", "value"),
    State("raw-data-store", "data"),
    prevent_initial_call=True,
)
def apply_encoding(n_clicks, columns, method, data):
    if n_clicks is None or not columns or method is None:
        return no_update, "Select categorical columns and an encoding method."

    df = store_to_df(data)

    if method == "onehot":
        df = pd.get_dummies(df, columns=columns, drop_first=True)
        msg = f"Applied one-hot encoding to: {', '.join(columns)}."
    else:  # label encoding (simple)
        for col in columns:
            df[col] = df[col].astype("category").cat.codes
        msg = f"Applied label encoding to: {', '.join(columns)}."

    return df_to_store(df), msg

# 7) Train-test split
@callback(
    Output("split-message", "children"),
    Input("btn-apply-split", "n_clicks"),
    State("split-target", "value"),
    State("split-train-size", "value"),
    State("raw-data-store", "data"),
    prevent_initial_call=True,
)
def apply_split(n_clicks, target, train_size, data):
    if n_clicks is None or target is None:
        return "Select a target column."

    df = store_to_df(data)
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=train_size, random_state=42
    )

    msg = (
        f"Train-test split done with train_size={train_size}.\n"
        f"X_train: {X_train.shape}, X_test: {X_test.shape}, "
        f"y_train: {y_train.shape}, y_test: {y_test.shape}"
    )

    return msg

# 8) Download processed dataset
@callback(
    Output("download-processed", "data"),
    Input("btn-download-processed", "n_clicks"),
    State("raw-data-store", "data"),
    prevent_initial_call=True,
)
def download_processed(n_clicks, data):
    df = store_to_df(data)
    return dcc.send_data_frame(df.to_csv, "processed_dataset.csv", index=False)

# -------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
