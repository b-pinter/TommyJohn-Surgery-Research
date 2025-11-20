import sys
import os

os.environ['DASH_SERVE_LOCALLY'] = 'True'

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Load data
baseball_data = pd.read_parquet('data_complete.parquet')
surgery_list = [0, 1]  # Hardcode this to avoid numpy issues

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=['style.css'])
server = app.server

app.layout = html.Div([
    html.H1("Pitching Viz"),

    html.H3("First Pitcher"),
    dcc.Dropdown(
        id='surgery_selection1',
        options=[{'label': '0 - No Surgery', 'value': 0},
                 {'label': '1 - Had Surgery', 'value': 1}],
        value=0
    ),
    html.Div(id='conditional_dropdown_container1'),
    dcc.Graph(id="pitch_location1"),

    html.H3("Second Pitcher"),
    dcc.Dropdown(
        id='surgery_selection2',
        options=[{'label': '0 - No Surgery', 'value': 0},
                 {'label': '1 - Had Surgery', 'value': 1}],
        value=0
    ),
    html.Div(id='conditional_dropdown_container2'),
    dcc.Graph(id="pitch_location2")
])


@app.callback(
    Output('conditional_dropdown_container1', 'children'),
    Input('surgery_selection1', 'value')
)
def update_players1(surgery_value):
    print(f"CALLBACK 1: surgery_value={surgery_value}, type={type(surgery_value)}")

    # Filter data
    filtered = baseball_data[baseball_data['surgery'] == surgery_value]
    print(f"CALLBACK 1: Found {len(filtered)} rows")

    # Get unique players
    players = filtered['player_name'].unique().tolist()
    print(f"CALLBACK 1: Found {len(players)} players")

    if len(players) == 0:
        return html.Div("No players found")

    # Sort players
    players = sorted(players)

    return html.Div([
        html.Label("Select Player:"),
        dcc.Dropdown(
            id='player_dropdown1',
            options=[{'label': p, 'value': p} for p in players],
            value=players[0]
        )
    ])


@app.callback(
    Output('conditional_dropdown_container2', 'children'),
    Input('surgery_selection2', 'value')
)
def update_players2(surgery_value):
    print(f"CALLBACK 2: surgery_value={surgery_value}, type={type(surgery_value)}")

    filtered = baseball_data[baseball_data['surgery'] == surgery_value]
    print(f"CALLBACK 2: Found {len(filtered)} rows")

    players = filtered['player_name'].unique().tolist()
    print(f"CALLBACK 2: Found {len(players)} players")

    if len(players) == 0:
        return html.Div("No players found")

    players = sorted(players)

    return html.Div([
        html.Label("Select Player:"),
        dcc.Dropdown(
            id='player_dropdown2',
            options=[{'label': p, 'value': p} for p in players],
            value=players[0]
        )
    ])


@app.callback(
    Output('pitch_location1', 'figure'),
    Input('player_dropdown1', 'value'),
    prevent_initial_call=True
)
def build_graph1(player):
    print(f"GRAPH 1: player={player}")
    filtered = baseball_data[baseball_data['player_name'] == player]

    fig = px.scatter(
        filtered,
        x='release_pos_x',
        y='plate_z',
        color='pitch_name',
        symbol='pitch_name',
        title=f'Pitch Location for {player}'
    )
    return fig


@app.callback(
    Output('pitch_location2', 'figure'),
    Input('player_dropdown2', 'value'),
    prevent_initial_call=True
)
def build_graph2(player):
    print(f"GRAPH 2: player={player}")
    filtered = baseball_data[baseball_data['player_name'] == player]

    fig = px.scatter(
        filtered,
        x='release_pos_x',
        y='plate_z',
        color='pitch_name',
        symbol='pitch_name',
        title=f'Pitch Location for {player}'
    )
    return fig


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)