from dash import dcc
from dash import html


def create_form():
    return html.Div([
        dcc.Input(id='input-1', value='Foodame', type='text'),
        dcc.Input(id='input-2', value='Calories', type='number'),
        dcc.Input(id='input-3', value='Protein', type='number'),
        dcc.Input(id='input-4', value='Date', type='text'),
        html.Button('Submit', id='submit-button'),
        html.Div(id='form-data')
    ])



