from doctest import debug

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from plotly.matplotlylib.mplexporter.renderers import fig_to_vega

app = Dash(__name__)

# -- Import and clean data (Importing csv into pandas)
df = pd.read_csv('intro_bees.csv')

df2 = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df2.reset_index(inplace=True)
print(df2[:5])

year_list = [i for i in range(2015, 2019, 1)]
app.layout = html.Div(children = [
    html.H1(children= 'Web Application Dashboards with Dash', style ={'text-align': 'center', 'font-size': '24px'}),
    html.Div(children=[
    dcc.Dropdown(
        id = 'select-year',
        options = [
            { 'label':i, 'value': i } for i in year_list
                ],
        multi = False,
        value = None,
        placeholder = 'Select a year',
        style = {'width':'40%', 'font-size': '20px', 'textAlign': 'center'}
    )
    ], style = {'marginBottom': '2em'}),

    html.Div(id = 'output_container', children= []),
    html.Br(),

    dcc.Graph(id='bee_map', figure={}),
    dcc.Graph(id='graph', figure={})

])

# Connect the Plotly graphs with Dash Components

@app.callback(
    [Output(component_id = 'output_container', component_property='children'),
     Output(component_id = 'bee_map', component_property='figure'),
     Output(component_id='graph', component_property='figure')],
     [Input(component_id='select-year', component_property='value'),
     ])

def update_graph(option_selected):
    print(option_selected)
    print(type(option_selected))
    container = f'The year chosen by user was: {option_selected}'

    dff = df2.copy()
    dff = dff[dff['Year'] == option_selected]
    dff = dff[dff['Affected by'] == 'Varroa_mites']

    #Plotly Express
    fig1=px.choropleth(
    data_frame = dff,
    locationmode = 'USA-states',
    locations = 'state_code',
    scope = 'usa',
    color = 'Pct of Colonies Impacted',
    hover_data=['State', 'Pct of Colonies Impacted'],
    color_continuous_scale = px.colors.sequential.YlOrRd,
    labels = {'Pct of Colonies Impacted': '% of Bee Colonies'},
    template = 'plotly_dark'
    )
    fig2 = px.bar(data_frame=dff,
                  x='State',
                  y='Pct of Colonies Impacted',
                  title = 'Percentage of Bee Colonies Per State')


    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)