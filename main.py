import dash
from dash import html, dash_table, dcc
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('aquarium.db')
cursor = conn.cursor()

# Initialize the app - incorporate css
external_stylesheets = ['/assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# SQL query
query = "select date, pH, ammonia, nitrite, nitrate, KH, GH from water_param"

# Fetch the results into a Pandas DataFrame
df = pd.read_sql_query(query, conn)

mode = "lines+markers"

# Define your layout
app.layout = html.Div([
    html.H1("Aquarium Water Parameter Visualiser v0.1"),
    
    dcc.Graph(
        id='line-chart',
        figure={}
    ),

    dcc.Checklist(
        className='series-selector',
        id='series-selector',
        options=[
            {'label': 'pH', 'value': 'pH'},
            {'label': 'Ammonia', 'value': 'ammonia'},
            {'label': 'Nitrite', 'value': 'nitrite'},
            {'label': 'Nitrate', 'value': 'nitrate'},
            {'label': 'KH', 'value': 'KH'},
            {'label': 'GH', 'value': 'GH'}
        ],
        value=['pH', 'ammonia', 'nitrite', 'nitrate', 'KH', 'GH'],
        inline=True
    )
])

# Callback to update the graph based on selected series
@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('series-selector', 'value')]
)
def update_graph(selected_series):
    data = []

    # Create a trace for each selected series
    for series in selected_series:
        data.append({'x': df['date'], 'y': df[series], 'mode': mode, 'name': series})

    return {
        'data': data,
        'layout': {
            'title': 'Water Quality over Time',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Values'},
            'hovermode': 'closest'
        }
    }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
