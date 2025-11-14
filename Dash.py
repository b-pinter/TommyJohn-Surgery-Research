#Import information
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
########################################################
#TO DO
#Add in conditional statements for the dropdown menu (Fixing issues with data visual)
#Seperate by pitchers who/who not have had surgery (Done)
#Allow to see pitch types use the figure building function found below
#Update style.css to make more pretty/color (look into how to do this)
########################################################

#Load in data (Cleaned)
baseball_data = pd.read_csv('baseball_data.csv')
player_list = baseball_data['player_name'].unique()
surgery_list = baseball_data['surgery'].unique()
#Boot up the dashboard
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets= ['style.css'])
app.layout = html.Div(children =[
    html.H1("Pitching Viz"),
    html.Label('Select type of Pitcher:'),
    dcc.Dropdown(
        id = 'surgery_selection',
        options = [{'label': surgery, 'value': surgery} for surgery in surgery_list],
        value = surgery_list[0]
    ),
    html.Div(id='conditional_dropdown_container'),
    dcc.Graph(id="pitch_location")

])

#First information update for conditional portion
@app.callback(
    Output('conditional_dropdown_container', 'children'),
    Input('surgery_selection', 'value')
)


#Conditional Statement for Dropdowns
def conditional_visual(selected_surgery):
    if selected_surgery == 0:
        select_filter = baseball_data[baseball_data['surgery'] == 0]
    else:
        select_filter = baseball_data[baseball_data['surgery'] == 1]
    surgery_players = select_filter['player_name'].unique()
    return html.Div([
        html.Label("Select Player:"),
        dcc.Dropdown(
            id='player_dropdown',
            options=[{'label': player, 'value': player} for player in surgery_players],
            value=surgery_players[0]
        )
    ])

#Second callback for the dropdown menus
@app.callback(
    Output('pitch_location', 'figure'),
    Input('player_dropdown', 'value')
)

#Build the pitching visual
def build_visual(player):
    pitching_filter = baseball_data[baseball_data['player_name'] == player]
    fig = px.scatter(
        pitching_filter,
        x = 'release_pos_x',
        y = 'plate_z',
        color = 'pitch_name',
        symbol = 'pitch_name',
        title = f'Pitch Location for {player}',
        labels = {'release_pos_x': 'Release Position X', 'plate_z' : 'Plate Z'}
    )
    return fig

#Running
if __name__ == "__main__":
    app.run(debug=True, port=8050)