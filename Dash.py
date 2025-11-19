# Imports
from dash import Dash, html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd

################################################################################################################
# Load in data (Cleaned)
print("Starting data load...")
try:
    baseball_data = pd.read_parquet('data_complete.parquet')
    print(f"✓ Data loaded: {len(baseball_data)} rows")
    player_list = baseball_data['player_name'].unique()
    surgery_list = sorted(baseball_data['surgery'].unique())
    print(f"✓ Players: {len(player_list)}, Surgery types: {surgery_list}")
except Exception as e:
    print(f"✗ ERROR: {e}")
    baseball_data = pd.DataFrame()
    player_list = []
    surgery_list = [0, 1]

# Boot up the dashboard
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=['style.css'])
server = app.server

app.layout = html.Div(children=[
    html.H1("Pitching Viz"),
    html.Label('Select type of Pitcher:'),
    html.Sup('0 for those who did not have Tommy John Surgery, 1 for those who had it.'),
    html.Div(children=[
        dcc.Dropdown(
            id='surgery_selection1',
            options=[{'label': str(surgery), 'value': surgery} for surgery in surgery_list],
            value=surgery_list[0] if len(surgery_list) > 0 else 0),

        html.Div(id='conditional_dropdown_container1'),
        dcc.Graph(id="pitch_location1"),

        html.Label('Select type of Pitcher:'),
        html.Sup('0 for those who did not have Tommy John Surgery, 1 for those who had it.'),
        dcc.Dropdown(
            id='surgery_selection2',
            options=[{'label': str(surgery), 'value': surgery} for surgery in surgery_list],
            value=surgery_list[0] if len(surgery_list) > 0 else 0),

        html.Div(id='conditional_dropdown_container2'),
        dcc.Graph(id="pitch_location2")
    ]),
])


# First callback
@app.callback(
    Output('conditional_dropdown_container1', 'children'),
    Input('surgery_selection1', 'value')
)
def conditional_visual1(selected_surgery):
    try:
        print(f"Callback 1 triggered with surgery: {selected_surgery}")

        if baseball_data.empty:
            return html.Div("Error: Data not loaded")

        select_filter = baseball_data[baseball_data['surgery'] == selected_surgery]
        surgery_players = sorted(select_filter['player_name'].unique())

        print(f"Found {len(surgery_players)} players for surgery={selected_surgery}")

        if len(surgery_players) == 0:
            return html.Div("No players found")

        return html.Div([
            html.Label("Select Player:"),
            html.Sup('Last,First Name'),
            dcc.Dropdown(
                id='player_dropdown1',
                options=[{'label': player, 'value': player} for player in surgery_players],
                value=surgery_players[0]
            )
        ])
    except Exception as e:
        print(f"✗ Error in callback 1: {e}")
        import traceback
        traceback.print_exc()
        return html.Div(f"Error: {str(e)}")


# Second callback
@app.callback(
    Output('conditional_dropdown_container2', 'children'),
    Input('surgery_selection2', 'value')
)
def conditional_visual2(selected_surgery):
    try:
        print(f"Callback 2 triggered with surgery: {selected_surgery}")

        if baseball_data.empty:
            return html.Div("Error: Data not loaded")

        select_filter = baseball_data[baseball_data['surgery'] == selected_surgery]
        surgery_players = sorted(select_filter['player_name'].unique())

        print(f"Found {len(surgery_players)} players for surgery={selected_surgery}")

        if len(surgery_players) == 0:
            return html.Div("No players found")

        return html.Div([
            html.Label("Select Player:"),
            html.Sup('Last,First Name'),
            dcc.Dropdown(
                id='player_dropdown2',
                options=[{'label': player, 'value': player} for player in surgery_players],
                value=surgery_players[0]
            )
        ])
    except Exception as e:
        print(f"✗ Error in callback 2: {e}")
        import traceback
        traceback.print_exc()
        return html.Div(f"Error: {str(e)}")


# Graph callback 1
@app.callback(
    Output('pitch_location1', 'figure'),
    Input('player_dropdown1', 'value'),
    prevent_initial_call=True
)
def build_visual1(player):
    try:
        print(f"Building graph 1 for player: {player}")
        pitching_filter = baseball_data[baseball_data['player_name'] == player]
        fig = px.scatter(
            pitching_filter,
            x='release_pos_x',
            y='plate_z',
            color='pitch_name',
            symbol='pitch_name',
            title=f'Pitch Location for {player}',
            labels={'release_pos_x': 'Release Position X', 'plate_z': 'Plate Z'}
        )
        return fig
    except Exception as e:
        print(f"✗ Error in graph 1: {e}")
        return px.scatter(title=f"Error: {str(e)}")


# Graph callback 2
@app.callback(
    Output('pitch_location2', 'figure'),
    Input('player_dropdown2', 'value'),
    prevent_initial_call=True
)
def build_visual2(player):
    try:
        print(f"Building graph 2 for player: {player}")
        pitching_filter = baseball_data[baseball_data['player_name'] == player]
        fig = px.scatter(
            pitching_filter,
            x='release_pos_x',
            y='plate_z',
            color='pitch_name',
            symbol='pitch_name',
            title=f'Pitch Location for {player}',
            labels={'release_pos_x': 'Release Position X', 'plate_z': 'Plate Z'}
        )
        return fig
    except Exception as e:
        print(f"✗ Error in graph 2: {e}")
        return px.scatter(title=f"Error: {str(e)}")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)