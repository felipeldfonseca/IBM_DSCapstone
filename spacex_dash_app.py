# Import required libraries
import pandas as pd
import dash as dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                       style={'textAlign': 'center', 'color': '#503D36',
                                              'font-size': 40}),
                               # TASK 1: Add a dropdown list to enable Launch Site selection
                               # The default select value is for ALL sites
                               # dcc.Dropdown(id='site-dropdown',...)
                               html.Br(),
                               dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),


                               # TASK 2: Add a pie chart to show the total successful launches count for all sites
                               # If a specific launch site was selected, show  Success vs. Failed counts for the site
                               html.Div(dcc.Graph(id='success-pie-chart')),
                               html.Br(),


                               html.P("Payload range (Kg):"),
                               # TASK 3: Add a slider to select payload range
                               # dcc.RangeSlider(id='payload-slider',...)
                               dcc.RangeSlider(id='payload-slider',
                                               min=0, max=10000, step=1000,
                                               marks={0: '0',
                                                      2500: '2500',
                                                      5000: '5000',
                                                      7500: '7500',
                                                      10000: '10000'},
                                               value=[min_payload, max_payload]),


                               # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                               html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                               ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
             Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
   # check if 'ALL' is selected
   if entered_site == 'ALL':
       # if 'ALL' is selected, a pie chart is created showing the proportion of launches from each launch site
       fig = px.pie(spacex_df, values='class', names='Launch Site',
                    title='Total Success Launches By Sites')
       # return the outcome piechart for a selected site
       return fig
   # if a specific launch site is selected
   else:
       # filter the dataframe to only show data from the selected launch site
       filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
       # Create a new data frame with two rows and 1 column
       counts_df = pd.DataFrame({'class': [0, 1]})
       # Filter the data of the column 'class' of the filtered_df (This is not a Data Frame, this is a pandas Series)
       class_df = filtered_df['class']
       # Group the rows by their values and count the occurrences of each value (pandas Series)
       counts = class_df.groupby(class_df).size()
       # Populate the counts into the new counts_df data frame
       counts_df['counts'] = counts.values
       # create a pie chart showing the proportion of the class outcomes for the selected launch site
       fig = px.pie(counts_df, values='counts', names='class',
                    title=f'Total Success Launches For Site {entered_site}')
       # return the outcome piechart for a selected site
       return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             Input(component_id='site-dropdown', component_property='value'),
             Input(component_id='payload-slider', component_property='value'))

def get_scatter_chart(entered_site, slider_payload):
   # Set high and low variables for the slider, so it can update itself
   low, high = slider_payload
   mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
   # Check if the entered site is 'ALL'
   if entered_site == 'ALL':
       # Create a scatter plot for 'ALL'
       fig = px.scatter(spacex_df[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category',
                        title='Correlation Between The Payload And Success For All Sites')
       return fig
   # Check if the entered site is 'CCAFS LC-40'
   elif entered_site == 'CCAFS LC-40':
       # Filter the original data frame to contain only the launches of CCAFS LC-40
       filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
       # Create a scatter plot for 'CCAFS LC-40'
       fig = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Correlation Between The Payload And Success for CCAFS LC-40')
       return fig
   # Check if the entered site is 'CCAFS SLC-40'
   elif entered_site == 'CCAFS SLC-40':
       # Filter the original data frame to contain only the launches of CCAFS SLC-40
       filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
       # Create a scatter plot for 'CCAFS SLC-40'
       fig = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Correlation Between The Payload And Success for CCAFS SLC-40')
       return fig
   # Check if the entered site is 'KSC LC-39A'
   elif entered_site == 'KSC LC-39A':
       # Filter the original data frame to contain only the launches of KSC LC-39A
       filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
       # Create a scatter plot for 'KSC LC-39A'
       fig = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Correlation Between The Payload And Success for KSC LC-39A')
       return fig
   # Check if the entered site is 'VAFB SLC-4E'
   elif entered_site == 'VAFB SLC-4E':
       # Filter the original data frame to contain only the launches of VAFB SLC-4E
       filtered_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
       # Create a scatter plot for 'VAFB SLC-4E'
       fig = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Correlation Between The Payload And Success for VAFB SLC-4E')
       return fig



# Run the app
if __name__ == '__main__':
   app.run_server()

