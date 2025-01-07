import pandas as pd
import plotly.express as px
from plotly.matplotlylib.mplexporter.renderers import fig_to_vega
from dash import Dash, dcc, html, Input, Output

#Initializa the app
app = Dash(__name__)

df = pd.read_csv('intro_bees.csv')

# Get the mean % of colonies according to the columns provided
df2 = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df2.reset_index(inplace=True)

app.layout= html.Div(children= [
    html.H1(children= 'Bees Population Based on different Factors', style = {'text-align': 'center', 'font-size': '24px'}),
    #styling input
    html.Div(children = [
        dcc.Dropdown(
            id = 'select-factor',
            options = [
                {'label': 'Disease', 'value': 'Disease' },
                {'label': 'Other', 'value': 'Other' },
                {'label': 'Pesticides', 'value': 'Pesticides' },
                {'label': 'Pests excluding Varroa', 'value': 'Pests_excl_Varroa' },
                {'label': 'Unknown', 'value': 'Unknown' },
                {'label': 'Varroa mites', 'value': 'Varroa_mites' },
                ],
            value = None,
            multi = False,
            placeholder = 'Select a factor to display',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        ),
    #Styling output Container
    html.Div(id = 'output-container', children = []),
    html.Br(),
    dcc.Graph(id = 'line-plot', figure = {})

    ])
])

@app.callback (
        [Output(component_id= 'output-container', component_property= 'children'),
         Output(component_id='line-plot', component_property='figure')],
         [Input(component_id='select-factor', component_property='value')
         ])

def update_graph(selected_input):
    container = f' The Impact of { selected_input} on Bee Colonies'
    df5 = df2.copy()
    df5 = df5[df5['Affected by'] == selected_input]
    df5 = df5[(df5["State"] == "Idaho") | (df5["State"] == "New York") | (df5["State"] == "New Mexico")]

    fig = px.line(data_frame = df5, x = 'Year',
                  y= 'Pct of Colonies Impacted',
                  color = 'State',
                  title = f'{selected_input}',
		          template = 'plotly_dark')

    return container, fig

if __name__ == '__main__':
    app.run_server(port = 8057, debug=True)



