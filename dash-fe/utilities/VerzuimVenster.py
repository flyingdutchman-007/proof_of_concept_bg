import requests
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.io as pio

class Dashboard:
    def __init__(self,query,kleur_emc):
        self.query = query
        self.kleur_emc = kleur_emc
        

    def query_data(self, query):
        try:
            response = requests.post('http://graphql:5015/graphql', json={'query': query})
            response.raise_for_status()
            data = response.json()
            data = data['data']['VerzuimVensterQuery'][0]
            
            return data

        except requests.exceptions.HTTPError as err:
            data = {'Naam': ['WVS', '1e Kwartiel'], 'Verzuimpercentage': [16.20025445292621, 14.838207128456654], 'GemiddeldeMeldingsfrequentie': [1.8223969465648853, 1.7360879993093987], 'label': ['WVS, 16.2%, 1.82', '1e Kwartiel, 14.8%, 1.74'], 'verzuimfreqVenster': 2.0106678147722925, 'verzuimpercVenster': 15.606863120295955}
            return data
        
        except requests.exceptions.RequestException as err:
            data = {'Naam': ['WVS', '1e Kwartiel'], 'Verzuimpercentage': [16.20025445292621, 14.838207128456654], 'GemiddeldeMeldingsfrequentie': [1.8223969465648853, 1.7360879993093987], 'label': ['WVS, 16.2%, 1.82', '1e Kwartiel, 14.8%, 1.74'], 'verzuimfreqVenster': 2.0106678147722925, 'verzuimpercVenster': 15.606863120295955}
            return data
            
    def plot_verzuimpercentage_vs_gemMeldingsfrequentie(self, data, kleur_emc):
        try:      
            verzuimfreqVenster = data.pop('verzuimfreqVenster')
            verzuimpercVenster = data.pop('verzuimpercVenster')
            df_verzuimpercentage_vs_gemMeldingsfrequentie  = pd.DataFrame(data)
            
            fig = px.scatter(
            df_verzuimpercentage_vs_gemMeldingsfrequentie, 
            x="Verzuimpercentage", 
            y="GemiddeldeMeldingsfrequentie", 
            color="Naam", 
            title="Verzuimvenster",
            text="label",
            color_discrete_sequence=kleur_emc
        )
            fig.update_layout(
                font_size = 14,
                font_family="Times",
                font_color="black",
                title_font_family="Times",
                title_font_color="black",
                legend_title_font_color="black"
            )
            max_x=24
            min_x=6
            max_y=3.4
            min_y=1
            
            fig.add_shape(
                type="rect",
                x0=min_x, y0=min_y,
                x1=verzuimpercVenster, y1=verzuimfreqVenster,
                fillcolor="green",opacity=0.25, line_width=0
            )
            fig.add_shape(
                type="rect",
                x0=min_x, y0=verzuimfreqVenster,
                x1=verzuimpercVenster, y1=max_y,
                fillcolor="yellow",opacity=0.25, line_width=0
            )
            fig.add_shape(
                type="rect",
                x0=verzuimpercVenster, y0=verzuimfreqVenster,
                x1=max_x, y1=max_y,
                fillcolor="red",opacity=0.25, line_width=0
            )
            fig.add_shape(
                type="rect",
                x0=verzuimpercVenster, y0=min_y,
                x1=max_x, y1=verzuimfreqVenster,
                fillcolor="orange",opacity=0.25, line_width=0
            )
            fig.add_trace(go.Scatter(
                x=[7, 7, 19, 19],
                y=[1.1, 3.2, 3.2, 1.1],
                text=["Laag verzuim probleem",
                    "Kort verzuim probleem",
                    "Dubbel verzuim probleem",
                    "Lang verzuim probleem"],
                mode="text",
            ))  
            fig.update_yaxes(range = [min_y,max_y])
            fig.update_xaxes(range = [min_x,max_x])
            fig.update_traces(marker={'size': 25}, textposition='top center', marker_opacity=1,selector=dict(type='scatter'))
            fig.update_layout(showlegend=False)

            return fig 
            
        except:
            return 'error'
        
    


    def create_dashoard(self):
        try:
            data = self.query_data(self.query)
            
            fig = self.plot_verzuimpercentage_vs_gemMeldingsfrequentie(data, self.kleur_emc)
            
            return html.Div([
                dcc.Graph(id='graph', figure=fig)
                ])
        except:
            return "error"





