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

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Test App"),
    dcc.Dropdown(id='test-dropdown', options=[{'label': '0', 'value': 0}, {'label': '1', 'value': 1}], value=0),
    html.Div(id='test-output')
])

@app.callback(
    Output('test-output', 'children'),
    Input('test-dropdown', 'value')
)
def test_callback(value):
    msg = f"CALLBACK FIRED! Value={value}"
    print(msg, file=sys.stderr)
    print(msg, flush=True)
    return html.Div(msg)

print("App configured, server starting...", file=sys.stderr)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)