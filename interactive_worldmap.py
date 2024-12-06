import pandas as pd
import os
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pycountry
from flask import Flask, send_from_directory

# Initialize the Flask server
server = Flask(__name__)

# Initialize the Dash app with the Flask server
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

# Load the dataset
df = pd.read_csv("C:/Users/cccar/Downloads/ds4200_project_co2_data.csv")

valid_country_codes = [country.alpha_3 for country in pycountry.countries]
df = df[df['iso_code'].isin(valid_country_codes)]
df = df.drop(index=3961)

# Layout for the app
app.layout = html.Div([

    # Dropdown for selecting the variable
    dcc.Dropdown(
        id="data-dropdown",
        options=[
            {"label": "CO2 Per Capita", "value": "co2_per_capita"},
            {"label": "CO2 Per GDP", "value": "co2_per_gdp"},
            {"label": "CO2 Per Unit Energy", "value": "co2_per_unit_energy"},
            {"label": "Cement CO2", "value": "cement_co2"},
            {"label": "Coal CO2", "value": "coal_co2"},
            {"label": "Flaring CO2", "value": "flaring_co2"},
            {"label": "Gas CO2", "value": "gas_co2"},
            {"label": "Land Use Change CO2", "value": "land_use_change_co2"},
            {"label": "Oil CO2", "value": "oil_co2"},
            {"label": "Trade CO2", "value": "trade_co2"},
            {"label": "Other Industry CO2", "value": "other_industry_co2"}
        ],
        value="co2_per_capita",  # Default selection
        clearable=False,
        style={"width": "50%", "margin": "auto"}
    ),

    # Choropleth map
    dcc.Graph(id="choropleth-map")
])

# Callback to update the map based on dropdown selection
@app.callback(
    Output("choropleth-map", "figure"),
    [Input("data-dropdown", "value")]
)
def update_map(selected_data):
    fig = px.choropleth(
        df,
        locations="iso_code",
        color=selected_data, 
        hover_name="country",
        animation_frame="year",
        color_continuous_scale="YlOrRd",
        title=f"{selected_data.replace('_', ' ').title()} by Country Over Time",
        projection="natural earth",
        range_color=[df[selected_data].min(), df[selected_data].max() * .75]
    )
    return fig

# Route to serve the HTML file
@server.route('/')
def index():
    return send_from_directory(os.getcwd(), 'interactive_worldmap.html')

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
