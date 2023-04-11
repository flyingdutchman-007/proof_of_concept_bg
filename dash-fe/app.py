import dash_mantine_components as dmc
from dash import Dash
from dash import html
from dash import callback
from dash import Input, Output


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



app = Dash(__name__)



app.layout = html.Div(children=[
    dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Verzuimvenster", value="1"),
                            dmc.Tab("Verzuimpercentage", value="2"),
                            dmc.Tab("Verzuimpercentage Geslacht", value="3"),
                        ]
                    ),
                ],
                id="tabs-example",
                value="1",
            ),
            html.Div(id="tabs-content", style={"paddingTop": 10}),
        ]
    )

@callback(Output("tabs-content", "children"), Input("tabs-example", "value"),suppress_callback_exceptions=True)
def render_content(active):
    if active == "1":
        return [dmc.Text("VerzuimVenster"), dashboard]
    elif active == '2':
        return [dmc.Text("Verzuimpercentage"), dashboard2]
    else: 
        return [dmc.Text("Verzuimpercentage Per Geslacht"),dashboard3]


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050,threaded=True)
