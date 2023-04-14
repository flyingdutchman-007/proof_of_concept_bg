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

class Dashboard4:
    def __init__(self,query,kleur_emc,):
        self.query = query
        self.kleur_emc = kleur_emc
        

    def query_data(self, query):
        try:
            response = requests.post('http://graphql:5015/graphql', json={'query': query})
            response.raise_for_status()
            data = response.json()
            data = data['data']['VerzuimPercentageGeslachtQuery'][0]


        except requests.exceptions.HTTPError as err:
            print(f"Error during API request: {err}")
            
        except requests.exceptions.RequestException as err:
            print(f"Something went wrong: {err}")
            
        return data
            
    def plot_verzuimpercentage_vs_gemMeldingsfrequentie(self, data, kleur_emc):
                
        df_verzuimduur_benchmark  = pd.DataFrame(data)
        fig = px.bar(df_verzuimduur_benchmark, x="Type Dienstverband", y="Aantal Dagen", color="Jaar", barmode="group", text_auto='.2f', color_discrete_sequence=kleur_emc)
        fig.update_traces(textfont_size=36, textangle=0, textposition="outside", cliponaxis=False)
        fig.update_layout(
        font_size = 36,
        font_family="Times",
        font_color="black",
        title_font_family="Times",
        title_font_color="black",
        legend_title_font_color="black",
        )

        return fig 


    def create_dashoard(self):
        
        data = self.query_data(self.query)
        
        fig = self.plot_verzuimpercentage_vs_gemMeldingsfrequentie(data, self.kleur_emc)
            
        return html.Div([
            dcc.Graph(id='graph', figure=fig)
            ])





