from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

#load the dataset
df = pd.read_csv('dataset.csv')
df.info()
print(df['crypto_name'].value_counts(dropna=False))

opts = []
crps = list(df['crypto_name'].unique())
for i in crps:
    opts.append({"label": i, "value": i})


#create the dash app
app = Dash(__name__)

#set up the app layout
app.layout = html.Div([
    html.H1("Web Dashboard about CryptoCurrencies", style={'text-align': 'center'}),

    dcc.Dropdown(id='slct_crypto',
                 options=opts,
                 multi=False,
                 value='Bitcoin',
                 style={'width': "40%"}
    ),
    dcc.Dropdown(id='slct_feature',
                 options=[
                     {"label": "Open", "value": 'open'},
                     {"label": "High", "value": 'high'},
                     {"label": "Low", "value": 'low'},
                     {"label": "Close", "value": 'close'},
                     {"label": "MarketCap", "value": 'marketCap'}],
                 multi=False,
                 value='marketCap',
                 style={'width': "40%"}
    ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_crypto_chart', figure={})
])


#set up the callback function
@app.callback(
    Output(component_id='output_container', component_property='children'),
    Output(component_id='my_crypto_chart', component_property='figure'),
    Input(component_id='slct_crypto', component_property='value'),
    Input(component_id='slct_feature', component_property='value'),
)
def update_graph(crypto_slctd, feature_slctd):
    print(crypto_slctd, feature_slctd)
    print(type(crypto_slctd), type(feature_slctd))

    container = "The crypto chosen by user was: {}. The feature chosen by user was: {}".format(crypto_slctd, feature_slctd)

    dff = df.copy()
    dff = dff[dff['crypto_name'] == crypto_slctd]
    feature = dff[feature_slctd]

    #plotly express
    fig = px.line(dff,
                  x='date',
                  y=feature,
                  title='Open, Close, High, Low, and MarketCap vs Date',
                  color_discrete_sequence=px.colors.qualitative.Plotly)

    return container, fig

#run local server
if __name__ == '__main__':
    app.run_server(debug=True)