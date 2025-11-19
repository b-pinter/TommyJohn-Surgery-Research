#Imports
from dash import Dash, html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd
################################################################################################################
#TO DO
#Add in conditional statements for the dropdown menu (Done)
#Seperate by pitchers who/who not have had surgery (Done)
#Allow to see pitch types use the figure building function found below (Done)
#Update style.css to make more pretty/color (Done)
#Add a second plot to allow for pitcher visual comparison (Done)
#Add pitch selection menu (Possible done for tomorrow)

#What I learned
#ORDER MATTERS
#Time spend debugging due to dash order:
#1.5 hours
################################################################################################################
#Load in data (Cleaned)
baseball_data = pd.read_parquet('data_complete.parquet')
player_list = baseball_data['player_name'].unique()
surgery_list = baseball_data['surgery'].unique()
#Boot up the dashboard
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets= ['style.css'])
app.layout = html.Div(children =[
    html.H1("Pitching Viz"),
    html.Label('Select type of Pitcher:'),
    html.Sup('0 for those who did not have Tommy John Surgery, 1 for those who had it.'),
    html.Div(children=[
        dcc.Dropdown(
            id = 'surgery_selection1',
            options = [{'label': surgery, 'value': surgery} for surgery in surgery_list],
            value = surgery_list[0]),

        html.Div(id='conditional_dropdown_container1'),
        #html.Div(id='pitch_selection1'),
        dcc.Graph(id="pitch_location1"),

       #Second graph, all calls are below.
    html.Label('Select type of Pitcher:'),
    html.Sup('0 for those who did not have Tommy John Surgery, 1 for those who had it.'),
        dcc.Dropdown(
            id='surgery_selection2',
            options=[{'label': surgery, 'value': surgery} for surgery in surgery_list],
            value=surgery_list[0]),

        html.Div(id='conditional_dropdown_container2'),
        #html.Div(id='pitch_selection2'),
        dcc.Graph(id="pitch_location2")
    ]),
])

#First call
@app.callback(
    Output('conditional_dropdown_container1', 'children'),
    Input('surgery_selection1', 'value'),
    prevent_initial_call=True

)

#First conditional dropdown
def conditional_visual1(selected_surgery):
    if selected_surgery == 0:
        select_filter = baseball_data[baseball_data['surgery'] == 0]
    else:
        select_filter = baseball_data[baseball_data['surgery'] == 1]
    surgery_players = select_filter['player_name'].unique()
    return html.Div([
        html.Label("Select Player:"),
        html.Sup('Last,First Name'),
        dcc.Dropdown(
            id='player_dropdown1',
            options=[{'label': player, 'value': player} for player in surgery_players],
            value=surgery_players[0]
        )
    ])

#Second callback for the other dropdown menu
@app.callback(
    Output('conditional_dropdown_container2', 'children'),
    Input('surgery_selection2', 'value'),
    prevent_initial_call=True
)

#Second conditional dropdown
def conditional_visual2(selected_surgery):
    if selected_surgery == 0:
        select_filter = baseball_data[baseball_data['surgery'] == 0]
    else:
        select_filter = baseball_data[baseball_data['surgery'] == 1]
    surgery_players = select_filter['player_name'].unique()
    return html.Div([
        html.Label("Select Player:"),
        html.Sup('Last,First Name'),
        dcc.Dropdown(
            id='player_dropdown2',
            options=[{'label': player, 'value': player} for player in surgery_players],
            value=surgery_players[0]
        )
    ])

#Second callback for the dropdown menus
@app.callback(
    Output('pitch_location1', 'figure'),
    Input('player_dropdown1', 'value')
)

#Visual for first dropdown
def build_visual1(player):
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

#Visual and call for second dropdown
@app.callback(
    Output('pitch_location2', 'figure'),
    Input('player_dropdown2', 'value')
)

def build_visual2(player):
    pitching_filter = baseball_data[baseball_data['player_name'] == player]
    #Working on
    #pitches_thrown = pitching_filter['pitch_name'].unique()
    #dcc.Dropdown(
    #    id='pitch_selection2',
    #    options=[{'label': pitch, 'value': pitch} for pitch in pitches_thrown],
    #    multi=True
    #)
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

#Running the file
server = app.server

if __name__ == '__main__':
    app.run(debug=False, host = '0.0.0.0', port = 8050)