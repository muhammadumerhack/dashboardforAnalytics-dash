from dash import html, dcc, dash_table, Input, Output, callback
import pandas as pd

layout = html.Div(className="relative w-full h-screen overflow-hidden flex flex-col items-center justify-center", children=[
    # Background Image Layer
    html.Div(className="absolute inset-0 z-0", style={
        'backgroundImage': 'url("/assets/background.jpg")',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'filter': 'brightness(0.4)'
    }),

    # Content Layer
    html.Div(className="relative z-10 w-4/5 max-w-4xl text-center space-y-6", children=[
        html.H1("Ecommerce Returns Prediction System", 
                className="text-5xl font-bold text-yellow-400 drop-shadow-lg mb-4"),
        
        html.P("Leveraging Machine Learning to analyze customer behavior, predict return probabilities, and optimize reverse logistics efficiency.",
               className="text-lg text-gray-200 leading-relaxed max-w-2xl mx-auto"),

        # Upload Area
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ', html.A('Select Dataset', className="font-bold text-yellow-400 cursor-pointer")
            ]),
            className="w-full md:w-2/3 mx-auto h-20 border-2 border-dashed border-gray-400 rounded-xl flex items-center justify-center bg-white/10 hover:bg-white/20 transition duration-300 backdrop-blur-sm cursor-pointer"
        ),
        html.Div(id='upload-status', className="text-sm text-green-400 font-mono mt-2"),

        # Navigation Links (Using dcc.Link instead of Buttons to fix callback error)
        html.Div(className="flex flex-wrap justify-center gap-4 mt-8", children=[
            dcc.Link("Univariate Analysis", href="/univariate", className="px-6 py-3 bg-blue-600 hover:bg-blue-500 rounded-lg shadow-lg text-white font-semibold transition no-underline"),
            dcc.Link("Bivariate Analysis", href="/bivariate", className="px-6 py-3 bg-blue-600 hover:bg-blue-500 rounded-lg shadow-lg text-white font-semibold transition no-underline"),
            dcc.Link("Preprocessing Pipeline", href="/preprocessing", className="px-6 py-3 bg-purple-600 hover:bg-purple-500 rounded-lg shadow-lg text-white font-semibold transition no-underline"),
        ]),
        
        # Data Preview Table
        html.Div(id='landing-table-container', className="mt-8 w-full overflow-x-auto rounded-lg shadow-2xl border border-white/20")
    ])
])

# Callback to show table preview
@callback(
    Output('landing-table-container', 'children'),
    Input('stored-data', 'data')
)
def display_table(data_json):
    if data_json is None: return None
    df = pd.read_json(data_json, orient='split')
    return dash_table.DataTable(
        data=df.head(5).to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': 'rgba(0,0,0,0.5)', 'color': 'white', 'fontWeight': 'bold'},
        style_cell={'backgroundColor': 'rgba(255,255,255,0.1)', 'color': 'white', 'border': '1px solid #444'},
    )