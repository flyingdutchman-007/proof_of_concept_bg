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

class Dashboard2:
    def __init__(self,query,kleur_emc,):
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
            data = data['data']['VerzuimPercentageGeslachtQuery'][0]

            return data

        except HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise

        except RequestException as e:
            logging.error(f"Request failed: {e}")
            raise
        
            
    def plot_verzuimpercentage_vs_gemMeldingsfrequentie(self, data, kleur_emc):
        
        try:
            df_verzuimpercentage_naar_type_dienstverband  = pd.DataFrame(data)
        
            
            fig = px.bar(df_verzuimpercentage_naar_type_dienstverband, x="TypeDienstverband", y="Verzuimpercentage", color="Jaar", barmode="group", text_auto='.2%', color_discrete_sequence=kleur_emc)
            fig.update_traces(textfont_size=24, textangle=0, textposition="outside", cliponaxis=False)
            fig.update_layout(
                font_size = 24,
                font_family="Times",
                font_color="black",
                title_font_family="Times",
                title_font_color="black",
                legend_title_font_color="black",
                yaxis_tickformat = '.0%'
            )
            return fig
        except:
            return "error" 


    def create_dashoard(self):
        
        try:
            data = self.query_data(self.query)
            
            fig = self.plot_verzuimpercentage_vs_gemMeldingsfrequentie(data, self.kleur_emc)
                
            return html.Div([
                dcc.Graph(id='graph', figure=fig)
                ])
        except:
            return "error"





