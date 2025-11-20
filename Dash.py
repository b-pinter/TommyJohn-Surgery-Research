import os

os.environ['DASH_SERVE_LOCALLY'] = 'True'

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import sys

print("=" * 60, file=sys.stderr)
print("APP STARTING", file=sys.stderr)
print("=" * 60, file=sys.stderr)

# Load data
baseball_data = pd.read_parquet('data_complete.parquet')
print(f"Data loaded: {len(baseball_data)} rows", file=sys.stderr)

app = Dash(__name__, suppress_callback_exceptions=True
server = app.server

app.layout = html.Div([
    html.H1("Pitching Viz"),

    html.H3("First Pitcher"),
    dcc.Dropdown(
        id='surgery_selection1',
        options=[{'label': '0 - No Surgery', 'value': 0}, {'label': '1 - Had Surgery', 'value': 1}],
        value=0
    ),
    html.Div(id='player_container1'),
    dcc.Graph(id="pitch_location1"),

    html.H3("Second Pitcher"),
    dcc.Dropdown(
        id='surgery_selection2',
        options=[{'label': '0 - No Surgery', 'value': 0}, {'label': '1 - Had Surgery', 'value': 1}],
        value=0
    ),
    html.Div(id='player_container2'),
    dcc.Graph(id="pitch_location2")
])


@app.callback(
    Output('player_container1', 'children'),
    Input('surgery_selection1', 'value')
)
def update_players1(surgery_value):
    print(f"CALLBACK 1 FIRED: surgery={surgery_value}", file=sys.stderr, flush=True)

    try:
        # Filter data
        filtered = baseball_data[baseball_data['surgery'] == surgery_value]
        print(f"  Filtered to {len(filtered)} rows", file=sys.stderr, flush=True)

        # Get unique players and convert to list
        players = filtered['player_name'].unique()
        players_list = sorted([str(p) for p in players])
        print(f"  Found {len(players_list)} players", file=sys.stderr, flush=True)

        if len(players_list) == 0:
            return html.Div("No players found")

        dropdown = dcc.Dropdown(
            id='player_dropdown1',
            options=[{'label': p, 'value': p} for p in players_list],
            value=players_list[0]
        )

        print(f"  Returning dropdown", file=sys.stderr, flush=True)
        return html.Div([
            html.Label("Select Player:"),
            dropdown
        ])

    except Exception as e:
        error_msg = f"ERROR in callback 1: {str(e)}"
        print(error_msg, file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return html.Div(f"Error: {str(e)}")


@app.callback(
    Output('player_container2', 'children'),
    Input('surgery_selection2', 'value')
)
def update_players2(surgery_value):
    print(f"CALLBACK 2 FIRED: surgery={surgery_value}", file=sys.stderr, flush=True)

    try:
        filtered = baseball_data[baseball_data['surgery'] == surgery_value]
        print(f"  Filtered to {len(filtered)} rows", file=sys.stderr, flush=True)

        players = filtered['player_name'].unique()
        players_list = sorted([str(p) for p in players])
        print(f"  Found {len(players_list)} players", file=sys.stderr, flush=True)

        if len(players_list) == 0:
            return html.Div("No players found")

        dropdown = dcc.Dropdown(
            id='player_dropdown2',
            options=[{'label': p, 'value': p} for p in players_list],
            value=players_list[0]
        )

        print(f"  Returning dropdown", file=sys.stderr, flush=True)
        return html.Div([
            html.Label("Select Player:"),
            dropdown
        ])

    except Exception as e:
        error_msg = f"ERROR in callback 2: {str(e)}"
        print(error_msg, file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return html.Div(f"Error: {str(e)}")


@app.callback(
    Output('pitch_location1', 'figure'),
    Input('player_dropdown1', 'value'),
    prevent_initial_call=True
)
def build_graph1(player):
    print(f"GRAPH 1: player={player}", file=sys.stderr, flush=True)

    import plotly.express as px
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
    print(f"GRAPH 2: player={player}", file=sys.stderr, flush=True)

    import plotly.express as px
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


print("App configured", file=sys.stderr)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)