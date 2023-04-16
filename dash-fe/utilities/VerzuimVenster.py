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
import logging
import requests
from requests.exceptions import RequestException, HTTPError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class Dashboard:
    def __init__(self,query,kleur_emc):
        self.query = query
        self.kleur_emc = kleur_emc
        

    def query_data(self, query):
        url = 'http://127.0.0.1:5020/graphql'
        retry_strategy = Retry(
            total=3,
            backoff_factor=40,
            status_forcelist=[500, 502, 503, 504],
            method_whitelist=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        try:
            response = http.post(url, json={'query': query})
            response.raise_for_status()
            data = response.json()
            data = data['data']['VerzuimVensterQuery'][0]

            return data

        except HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise

        except RequestException as e:
            logging.error(f"Request failed: {e}")
            raise
            
    def plot_verzuimpercentage_vs_gemMeldingsfrequentie(self, data, kleur_emc):   
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
            
    


    def create_dashoard(self):
        try:
            data = self.query_data(self.query)
            
            fig = self.plot_verzuimpercentage_vs_gemMeldingsfrequentie(data, self.kleur_emc)
            
            return html.Div([
                dcc.Graph(id='graph3', figure=fig)
                ])
        except:
            return "error"





