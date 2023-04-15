from dash import Dash
from dash import html
from dash import callback
from dash import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc


from utilities.VerzuimVenster import Dashboard
from utilities.Verzuimpercentage import Dashboard2
from utilities.VerzuimpercentageGeslacht import Dashboard3


query = """
       query {
        VerzuimVensterQuery{
            Naam
            Verzuimpercentage
            GemiddeldeMeldingsfrequentie
            label
            verzuimfreqVenster
            verzuimpercVenster
        }
        }
        """
        

query2 = """
       query {
        VerzuimPercentageQuery{
            TypeDienstverband
            Jaar
            Verzuimpercentage
        }
        }
        """  
 
       
query3 = """
       query {
        VerzuimPercentageGeslachtQuery{
            TypeDienstverband
            Geslacht
            Verzuimpercentage
        }
        }
        """        

        
kleur_emc = ["#F29000","#252B5F","#E9501A","#adadad","#1F2C84"]

dashboard = Dashboard(query,kleur_emc)
dashboard = dashboard.create_dashoard()

dashboard2 = Dashboard2(query2,kleur_emc)
dashboard2 = dashboard2.create_dashoard()

dashboard3 = Dashboard3(query3,kleur_emc)
dashboard3 = dashboard3.create_dashoard()



app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])



# App layout
app.layout = html.Div(
    [
        navbar,
        html.Div(
            [
                html.H2("Dashboard 1"),
                dashboard1,
            ],
            style={"padding": "20px"},
        ),
        html.Div(
            [
                html.H2("Dashboard 2"),
                dashboard2,
            ],
            style={"padding": "20px"},
        ),
        html.Div(
            [
                html.H2("Dashboard 3"),
                dashboard3,
            ],
            style={"padding": "20px"},
        ),
    ]
)



if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050,threaded=True)
