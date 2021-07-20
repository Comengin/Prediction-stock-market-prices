import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash()
server = app.server

df = pd.read_csv("tickers.csv")
predfile = pd.read_csv("predictions.csv")
app.layout = html.Div([
    html.Div([
        html.H1("Close Price of Stocks",
                style={'textAlign': 'center'}),
        dcc.Dropdown(id='my-dropdown',
                     options=[{'label': 'Tesla', 'value': 'TSLA'},
                              {'label': 'Apple', 'value': 'AAPL'},
                              {'label': 'Facebook', 'value': 'FB'},
                              {'label': 'Microsoft', 'value': 'MSFT'},
                              {'label': 'Google ', 'value': 'GOOGL'}],
                     multi=True, value=['FB'],
                     style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "60%"}),
        dcc.Graph(id='close'),
    ], className="container"),
])


@app.callback(Output('close', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown):
    dropdown = {"TSLA": "Tesla", "AAPL": "Apple", "FB": "Facebook", "MSFT": "Microsoft", "GOOGL": "Google"}
    file1 = []
    file2 = []
    for stock in selected_dropdown:
        file1.append(
            go.Scatter(x=df[df["Stock"] == stock]["Date"], y=df[df["Stock"] == stock]["Close"],
                       mode='lines', opacity=0.7, name=f'Close {dropdown[stock]}', textposition='bottom center'))
        file2.append(
            go.Scatter(x=predfile[predfile["Stock"] == stock]["Date"], y=predfile[predfile["Stock"] == stock]["Predictions"],
                       mode='lines', opacity=0.6, name=f'Predictions {dropdown[stock]}', textposition='bottom center'))
    traces = [file1, file2]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1',
                                            '#FF7400', '#FFF400', '#FF0056'],
                                  height=600,
                                  title=f"Close Prices for {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
                                  xaxis={"title": "Date",
                                         'rangeselector': {'buttons': list(
                                             [{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                              {'count': 3, 'label': '3M', 'step': 'month', 'stepmode': 'backward'},
                                              {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                              {'step': 'all'}])},
                                         'rangeslider': {'visible': True}, 'type': 'date'},
                                  yaxis={"title": "Price (USD)"})}
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
