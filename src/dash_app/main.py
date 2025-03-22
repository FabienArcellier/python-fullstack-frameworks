import dash
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import requests
import traceback

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create a simple DataFrame with sample data in case the API fails
sample_data = [
    {'Name': 'Sample Mission', 'Date': '2023-01-01', 'Launcher': 'Sample Launcher', 'Launch Site': 'Sample Site', 'Mission': 'Sample Mission', 'Status': 'Success'},
]

try:
    def fetch_space_launches():
        """Fetch space launch data from Launch Library API."""
        try:
            url = "https://ll.thespacedevs.com/2.2.0/launch/previous/?limit=200&mode=detailed"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()['results']
            else:
                print(f"API returned status code {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []

    def process_launch_data(launches):
        """Process launch data into a DataFrame."""
        if not launches:
            print("Using sample data due to empty launches")
            return pd.DataFrame(sample_data)

        launch_data = []
        for launch in launches:
            try:
                launch_data.append({
                    'Name': launch.get('name', 'Unknown'),
                    'Date': launch.get('net', 'Unknown'),
                    'Launcher': launch.get('rocket', {}).get('configuration', {}).get('name', 'Unknown'),
                    'Launch Site': launch.get('pad', {}).get('location', {}).get('name', 'Unknown'),
                    'Mission': launch.get('mission', {}).get('name', 'Unknown') if launch.get('mission') else 'Unknown',
                    'Status': launch.get('status', {}).get('name', 'Unknown') if launch.get('status') else 'Unknown'
                })
            except Exception as e:
                print(f"Error processing launch: {e}")
                continue

        return pd.DataFrame(launch_data)

    # Fetch and process launch data
    launches = fetch_space_launches()
    df = process_launch_data(launches)

    # Ensure Date column is properly formatted
    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        # Replace NaT values with a default date
        df['Date'] = df['Date'].fillna(pd.Timestamp('2023-01-01'))
    except Exception as e:
        print(f"Error converting dates: {e}")
        # Create a simple date column if conversion fails
        df['Date'] = pd.to_datetime('2023-01-01')

    # Sort chronologically (newest first)
    df = df.sort_values('Date', ascending=False)

    # Create Month column for timeline
    df['Month'] = df['Date'].dt.strftime('%Y-%m')

    # Create monthly launches data
    monthly_launches = df.groupby('Month').size().reset_index(name='Launches')
    monthly_launches = monthly_launches.sort_values('Month')

except Exception as e:
    print(f"Error during initialization: {e}")
    traceback.print_exc()
    # Fallback to sample data
    df = pd.DataFrame(sample_data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    monthly_launches = df.groupby('Month').size().reset_index(name='Launches')

# App layout
try:
    app.layout = dbc.Container([
        html.H1("Space Missions Dashboard", className="text-center my-4"),
        html.H4("Chronological List of the Last 200 Space Missions", className="text-center mb-4"),

        dbc.Row([
            dbc.Col([
                html.H4("Filters"),
                dcc.Dropdown(
                    id='launcher-dropdown',
                    options=[{'label': i, 'value': i} for i in sorted(df['Launcher'].unique())],
                    multi=True,
                    placeholder="Filter by Launcher"
                ),
                html.Br(),
                dcc.Dropdown(
                    id='site-dropdown',
                    options=[{'label': i, 'value': i} for i in sorted(df['Launch Site'].unique())],
                    multi=True,
                    placeholder="Filter by Launch Site"
                )
            ], width=3),

            dbc.Col([
                dash_table.DataTable(
                    id='launch-table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    sort_action='native',
                    filter_action='native',
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '8px',
                        'minWidth': '100px', 'width': '150px', 'maxWidth': '200px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ]
                )
            ], width=9)
        ]),

        dbc.Row([
            dbc.Col([
                html.H4("Launch Timeline", className="text-center mt-4"),
                dcc.Graph(
                    id='monthly-launches-chart',
                    figure=px.bar(
                        monthly_launches,
                        x='Month',
                        y='Launches',
                        title='Number of Launches per Month'
                    ).update_layout(xaxis_title="Month", yaxis_title="Number of Launches")
                )
            ])
        ])
    ], fluid=True)
except Exception as e:
    print(f"Error creating layout: {e}")
    traceback.print_exc()
    # Fallback to minimal layout
    app.layout = html.Div([
        html.H1("Space Missions Dashboard", style={"textAlign": "center"}),
        html.P("Error loading data. Please try again later.", style={"textAlign": "center", "color": "red"})
    ])

@app.callback(
    [Output('launch-table', 'data'),
     Output('monthly-launches-chart', 'figure')],
    [Input('launcher-dropdown', 'value'),
     Input('site-dropdown', 'value')]
)
def update_dashboard(selected_launchers, selected_sites):
    try:
        filtered_df = df.copy()

        if selected_launchers:
            filtered_df = filtered_df[filtered_df['Launcher'].isin(selected_launchers)]

        if selected_sites:
            filtered_df = filtered_df[filtered_df['Launch Site'].isin(selected_sites)]

        # Update table
        table_data = filtered_df.to_dict('records')

        # Update monthly launches chart
        monthly_data = filtered_df.groupby('Month').size().reset_index(name='Launches')
        monthly_data = monthly_data.sort_values('Month')

        fig = px.bar(
            monthly_data,
            x='Month',
            y='Launches',
            title='Number of Launches per Month'
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="Number of Launches")

        return table_data, fig
    except Exception as e:
        print(f"Error in callback: {e}")
        traceback.print_exc()
        # Return empty data and a simple figure on error
        empty_fig = px.bar(
            pd.DataFrame({'Month': ['2023-01'], 'Launches': [0]}),
            x='Month',
            y='Launches',
            title='Error loading data'
        )
        return [], empty_fig

if __name__ == '__main__':
    app.run_server(debug=True)
