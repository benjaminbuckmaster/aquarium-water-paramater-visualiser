import dash
from dash import html, dcc
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('aquarium.db')
cursor = conn.cursor()

# Initialize the app
app = dash.Dash(__name__, title="Aquarium Water Parameter Visualiser")

# SQL query
query = "select date, pH, ammonia, nitrite, nitrate, KH, GH from water_param"

# Fetch the results into a Pandas DataFrame
df = pd.read_sql_query(query, conn)

# Graph customisation
graph_mode = "lines+markers"
colors = {
    'card': 'rgba(255,255,255,0.1)',
    'plot': 'rgba(255,255,255,0)',
    'legend': 'rgba(255,255,255,0)',
    'text': 'rgba(59, 59, 128,0.8)',
    'xaxis_color': 'rgba(59, 59, 128,0.8)',
    'yaxis_color': 'rgba(59, 59, 128,0.8)',
    'gridcolor': 'rgba(59, 59, 128,0.1)'
}

# Define your layout
app.layout = html.Div([
    html.H1("Aquarium Water Parameter Visualiser"),
    
    dcc.Graph(
        id='line-chart',
        figure={
            'data': [
                {'x': df['date'], 'y': df['pH'], 'mode': graph_mode, 'name': 'pH'},
                {'x': df['date'], 'y': df['ammonia'], 'mode': graph_mode, 'name': 'Ammonia'},
                {'x': df['date'], 'y': df['nitrite'], 'mode': graph_mode, 'name': 'Nitrite'},
                {'x': df['date'], 'y': df['nitrate'], 'mode': graph_mode, 'name': 'Nitrate'},
                {'x': df['date'], 'y': df['KH'], 'mode': graph_mode, 'name': 'KH'},
                {'x': df['date'], 'y': df['GH'], 'mode': graph_mode, 'name': 'GH'}
            ],
            'layout': {
                'title': 'Water Quality over Time',
                'xaxis': {'title': 'Date', 'linecolor': colors['xaxis_color'], 'gridcolor': colors['gridcolor']},
                'yaxis': {'title': 'Values', 'linecolor': colors['yaxis_color'], 'gridcolor': colors['gridcolor']},
                'hovermode': 'closest',
                'plot_bgcolor': colors['plot'],
                'paper_bgcolor': colors['card'],
                'font': {'color': colors['text']},
                'legend': {'bgcolor':colors['legend']}
            }
        }
    ) 
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
