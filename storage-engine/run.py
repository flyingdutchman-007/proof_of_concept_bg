from flask import Flask, jsonify
import pandas as pd
import numpy as np
from collections import OrderedDict

path = "/app/storage-engine/data.xlsx"


app = Flask(__name__)

#adding a route to the flask server with the url /sum
@app.route('/query-data',methods=['GET'])
def query_verzuimvenster():
    df_data = pd.read_excel(path, sheet_name="Data")
    df_kwartielen_500 = pd.read_excel(path, sheet_name="Kwartielen <500")
    df_kwartielen_500_1000 = pd.read_excel(path, sheet_name="Kwartielen <1000")
    df_kwartielen_1000_1500 = pd.read_excel(path, sheet_name="Kwartielen <1500")
    df_kwartielen_1500 = pd.read_excel(path, sheet_name="Kwartielen >1500")
    df_samenvatting_2 = pd.read_excel(path, sheet_name="KwartielenTotaal(samenvatting2)")
    df_grootteklasse = pd.read_excel(path, sheet_name="Grootteklasse")

    quartile_grootteklasse_500 = np.quantile(df_kwartielen_500['totaal verzuimpercentage 4e kwartaal 2022'], [0.25]).tolist()
    quartile_grootteklasse_500_1000 = np.quantile(df_kwartielen_500_1000['totaal verzuimpercentage 4e kwartaal 2022'], [0.25]).tolist()
    quartile_grootteklasse_1000_1500 = np.quantile(df_kwartielen_1000_1500['totaal verzuimpercentage 4e kwartaal 2022'], [0.25]).tolist()
    quartile_grootteklasse_1500 = np.quantile(df_kwartielen_1500['totaal verzuimpercentage 4e kwartaal 2022'], [0.25]).tolist()
    quartile_grootteklasse_totaal = np.quantile(df_samenvatting_2['totaal verzuimpercentage 4e kwartaal 2022'], [0.25]).tolist()

    quartile_grootteklasse_verzuimfrequentie_500 = np.quantile(df_kwartielen_500['totaal meldingsfrequentie 4e kwartaal2022'], [0.25]).tolist()
    quartile_grootteklasse_verzuimfrequentie_500_1000 = np.quantile(df_kwartielen_500_1000['totaal meldingsfrequentie 4e kwartaal2022'], [0.25]).tolist()
    quartile_grootteklasse_verzuimfrequentie_1000_1500 = np.quantile(df_kwartielen_1000_1500['totaal meldingsfrequentie 4e kwartaal2022'], [0.25]).tolist()
    quartile_grootteklasse_verzuimfrequentie_1500 = np.quantile(df_kwartielen_1500['totaal meldingsfrequentie 4e kwartaal2022'], [0.25]).tolist()
    quartile_grootteklasse_verzuimfrequentie_totaal = np.quantile(df_samenvatting_2['totaal meldingsfrequentie 4e kwartaal2022'], [0.25]).tolist()

    list_quartiles_verzuimpercentage = [quartile_grootteklasse_500, quartile_grootteklasse_500_1000, quartile_grootteklasse_1000_1500, quartile_grootteklasse_1500, quartile_grootteklasse_totaal]

    list_quartiles_verzuimfrequentie = [quartile_grootteklasse_verzuimfrequentie_500, quartile_grootteklasse_verzuimfrequentie_500_1000, quartile_grootteklasse_verzuimfrequentie_1000_1500, quartile_grootteklasse_verzuimfrequentie_1500, quartile_grootteklasse_verzuimfrequentie_totaal]

    df_quartiles_verzuimpercentage = pd.DataFrame(list_quartiles_verzuimpercentage, columns={ 'Verzuimpercentage' })
    df_quartiles_verzuimfrequentie = pd.DataFrame(list_quartiles_verzuimfrequentie, columns={ 'Verzuimfrequentie' })
    
    print (df_grootteklasse)
    df_data_dict = df_data.to_dict(orient='records')
    df_grootteklasse_dict = df_grootteklasse.to_dict(orient='records')
    df_quartiles_verzuimpercentage_dict = df_quartiles_verzuimpercentage.to_dict(orient='records')
    df_quartiles_verzuimfrequentie_dict = df_quartiles_verzuimfrequentie.to_dict(orient='records')

    # convert dataframes to ordered dictionaries
    df_data_dict = [OrderedDict(row) for row in df_data.to_dict(orient='records')]
    df_grootteklasse_dict = [OrderedDict(row) for row in df_grootteklasse.to_dict(orient='records')]
    df_quartiles_verzuimpercentage_dict = [OrderedDict(row) for row in df_quartiles_verzuimpercentage.to_dict(orient='records')]
    df_quartiles_verzuimfrequentie_dict = [OrderedDict(row) for row in df_quartiles_verzuimfrequentie.to_dict(orient='records')]

    # create a dictionary containing the ordered dictionaries
    data = {
        'df_data': df_data_dict,
        'df_grootteklasse': df_grootteklasse_dict,
        'df_quartiles_verzuimpercentage': df_quartiles_verzuimpercentage_dict,
        'df_quartiles_verzuimfrequentie': df_quartiles_verzuimfrequentie_dict
    }
    # Return the dictionary as JSON data
    # return jsonify(dfs)
    return jsonify(data)
    

# #adding a route to the flask server with the url /sum
# @app.route("/insert-food",methods=['POST'])
# def insert_food():
#     data = request.get_json()
#     connection.insert_food(data)
#     return "Data received", 200

# #adding a route to the flask server with the url /sum
# @app.route("/query-calcfood",methods=['GET'])
# def query_calcfood():
#     data = connection.query_calc_food()
#     return jsonify(data)

# #adding a route to the flask server with the url /sum
# @app.route("/insert-calcfood",methods=['POST'])
# def insert_calcfood():
#     data = request.get_json()
#     connection.insert_calc_food(data)
#     return "Data received", 200

#running the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5006,threaded=True)