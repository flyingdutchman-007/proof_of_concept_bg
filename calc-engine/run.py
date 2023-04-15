#importing modules
from flask import Flask, jsonify
import os
import requests
import pandas as pd
import numpy as np
import math

#importing classes
from utilities import push
from utilities import pull
from utilities import calculator

def def_grootteklasse_verzuimpercentage(num_grootteklasse):
    global grootteklasse
    grootteklasse = 0
    if num_grootteklasse == 'nvt':
        grootteklasse = 0
    elif num_grootteklasse >= 0 and num_grootteklasse < 500:
        grootteklasse = df_grootteklasse.iloc[0,1]*100
    elif num_grootteklasse >= 500 and num_grootteklasse < 1000:
        grootteklasse = df_grootteklasse.iloc[1,1]*100
    elif num_grootteklasse >= 1000 and num_grootteklasse < 1500:
        grootteklasse = df_grootteklasse.iloc[2,1]*100
    elif num_grootteklasse >= 1500:
        grootteklasse = df_grootteklasse.iloc[3,1]*100
    return grootteklasse

def def_grootteklasse_verzuimfrequentie(num_grootteklasse_verzuifrequentie):
    global grootteklasse
    grootteklasse = 0
    if num_grootteklasse_verzuifrequentie == 'nvt':
        grootteklasse = 0
    elif num_grootteklasse_verzuifrequentie >= 0 and num_grootteklasse_verzuifrequentie < 500:
        grootteklasse = df_grootteklasse.iloc[0,3]
    elif num_grootteklasse_verzuifrequentie >= 500 and num_grootteklasse_verzuifrequentie < 1000:
        grootteklasse = df_grootteklasse.iloc[1,3]
    elif num_grootteklasse_verzuifrequentie >= 1000 and num_grootteklasse_verzuifrequentie < 1500:
        grootteklasse = df_grootteklasse.iloc[2,3]
    elif num_grootteklasse_verzuifrequentie >= 1500:
        grootteklasse = df_grootteklasse.iloc[3,3]
    return grootteklasse

def def_kwartielen_verzuimfrequentie (num_kwartielen_verzuimfrequentie):
    global kwartielen
    if num_kwartielen_verzuimfrequentie == 'nvt':
        kwartielen = 0
    elif num_kwartielen_verzuimfrequentie >= 0 and num_kwartielen_verzuimfrequentie < 500:
        kwartielen = df_quartiles_verzuimfrequentie.iloc[0,0]
    elif num_kwartielen_verzuimfrequentie >= 500 and num_kwartielen_verzuimfrequentie < 1000:
        kwartielen = df_quartiles_verzuimfrequentie.iloc[1,0]
    elif num_kwartielen_verzuimfrequentie >= 1000 and num_kwartielen_verzuimfrequentie < 1500:
        kwartielen = df_quartiles_verzuimfrequentie.iloc[2,0]
    elif num_kwartielen_verzuimfrequentie >= 1500:
        kwartielen = df_quartiles_verzuimfrequentie.iloc[3,0]
    return kwartielen

def def_kwartielen_verzuimpercentage (num_kwartielen):
    global kwartielen
    if num_kwartielen == 'nvt':
        kwartielen = 0
    elif num_kwartielen >= 0 and num_kwartielen < 500:
        kwartielen = df_quartiles_verzuimpercentage.iloc[0,0]
    elif num_kwartielen >= 500 and num_kwartielen < 1000:
        kwartielen = df_quartiles_verzuimpercentage.iloc[1,0]
    elif num_kwartielen >= 1000 and num_kwartielen < 1500:
        kwartielen = df_quartiles_verzuimpercentage.iloc[2,0]
    elif num_kwartielen >= 1500:
        kwartielen = df_quartiles_verzuimpercentage.iloc[3,0]
    return kwartielen

def def_grootteklasse_verzuimduur(num_grootteklasse_verzuimduur):
    global grootteklasse
    grootteklasse = 0
    if num_grootteklasse_verzuimduur == 'nvt':
        grootteklasse = 0
    elif num_grootteklasse_verzuimduur >= 0 and num_grootteklasse_verzuimduur < 500:
        grootteklasse = df_grootteklasse.iloc[0,2]
    elif num_grootteklasse_verzuimduur >= 500 and num_grootteklasse_verzuimduur < 1000:
        grootteklasse = df_grootteklasse.iloc[1,2]
    elif num_grootteklasse_verzuimduur >= 1000 and num_grootteklasse_verzuimduur < 1500:
        grootteklasse = df_grootteklasse.iloc[2,2]
    elif num_grootteklasse_verzuimduur >= 1500:
        grootteklasse = df_grootteklasse.iloc[3,2]
    return grootteklasse

#creating the flask app variable
app = Flask(__name__)

#adding a route to the flask server with the url /sum
@app.route("/verzuimvenster", methods=['GET'])
def calc():
    response = requests.get('http://storage-service:9000/query-data')
    if response.status_code == 200:
        data = response.json()
        
        df_grootteklasse_dict = {}
        df_grootteklasse__list_dict = data['df_grootteklasse']
        for item in df_grootteklasse__list_dict:
            df_grootteklasse_dict[item['Grootteklasse']] = {
                'Verzuimpercentage': item['Verzuimpercentage'],
                'Verzuimduur': item['Verzuimduur'],
                'Meldingsfrequentie': item['Meldingsfrequentie']
            }
            
        
        df_data= pd.DataFrame.from_dict(data['df_data'])
        df_grootteklasse = pd.DataFrame.from_dict(df_grootteklasse_dict)
        df_grootteklasse = df_grootteklasse.T
        df_grootteklasse = df_grootteklasse.rename_axis("Grootteklasse").reset_index(drop=False)
        df_quartiles_verzuimpercentage = pd.DataFrame.from_dict(data['df_quartiles_verzuimpercentage'])
        df_quartiles_verzuimfrequentie = pd.DataFrame.from_dict(data['df_quartiles_verzuimfrequentie'])
        
        ## Calculaties invoegen met betrekking tot de kwartielen
        ## Calculaties invoegen met betrekking tot de kwartielen
        
        def def_grootteklasse_verzuimpercentage(num_grootteklasse):
            global grootteklasse
            grootteklasse = 0
            if num_grootteklasse == 'nvt':
                grootteklasse = 0
            elif num_grootteklasse >= 0 and num_grootteklasse < 500:
                grootteklasse = df_grootteklasse.iloc[0,1]*100
            elif num_grootteklasse >= 500 and num_grootteklasse < 1000:
                grootteklasse = df_grootteklasse.iloc[1,1]*100
            elif num_grootteklasse >= 1000 and num_grootteklasse < 1500:
                grootteklasse = df_grootteklasse.iloc[2,1]*100
            elif num_grootteklasse >= 1500:
                grootteklasse = df_grootteklasse.iloc[3,1]*100
            return grootteklasse

        def def_grootteklasse_verzuimfrequentie(num_grootteklasse_verzuifrequentie):
            global grootteklasse
            grootteklasse = 0
            if num_grootteklasse_verzuifrequentie == 'nvt':
                grootteklasse = 0
            elif num_grootteklasse_verzuifrequentie >= 0 and num_grootteklasse_verzuifrequentie < 500:
                grootteklasse = df_grootteklasse.iloc[0,3]
            elif num_grootteklasse_verzuifrequentie >= 500 and num_grootteklasse_verzuifrequentie < 1000:
                grootteklasse = df_grootteklasse.iloc[1,3]
            elif num_grootteklasse_verzuifrequentie >= 1000 and num_grootteklasse_verzuifrequentie < 1500:
                grootteklasse = df_grootteklasse.iloc[2,3]
            elif num_grootteklasse_verzuifrequentie >= 1500:
                grootteklasse = df_grootteklasse.iloc[3,3]
            return grootteklasse

        def def_kwartielen_verzuimfrequentie (num_kwartielen_verzuimfrequentie):
            global kwartielen
            if num_kwartielen_verzuimfrequentie == 'nvt':
                kwartielen = 0
            elif num_kwartielen_verzuimfrequentie >= 0 and num_kwartielen_verzuimfrequentie < 500:
                kwartielen = df_quartiles_verzuimfrequentie.iloc[0,0]
            elif num_kwartielen_verzuimfrequentie >= 500 and num_kwartielen_verzuimfrequentie < 1000:
                kwartielen = df_quartiles_verzuimfrequentie.iloc[1,0]
            elif num_kwartielen_verzuimfrequentie >= 1000 and num_kwartielen_verzuimfrequentie < 1500:
                kwartielen = df_quartiles_verzuimfrequentie.iloc[2,0]
            elif num_kwartielen_verzuimfrequentie >= 1500:
                kwartielen = df_quartiles_verzuimfrequentie.iloc[3,0]
            return kwartielen
    
        def def_kwartielen_verzuimpercentage (num_kwartielen):
            global kwartielen
            if num_kwartielen == 'nvt':
                kwartielen = 0
            elif num_kwartielen >= 0 and num_kwartielen < 500:
                kwartielen = df_quartiles_verzuimpercentage.iloc[0,0]
            elif num_kwartielen >= 500 and num_kwartielen < 1000:
                kwartielen = df_quartiles_verzuimpercentage.iloc[1,0]
            elif num_kwartielen >= 1000 and num_kwartielen < 1500:
                kwartielen = df_quartiles_verzuimpercentage.iloc[2,0]
            elif num_kwartielen >= 1500:
                kwartielen = df_quartiles_verzuimpercentage.iloc[3,0]
            return kwartielen
    
        company_list = []
        for bedrijf in df_data.index:
            
            srs_bdrf = df_data.iloc[bedrijf]
            wsw_dienstverband_man = srs_bdrf['manWSW']
            wsw_dienstverband_vrouw = srs_bdrf['vrouwWSW']
            ander_dienstverband_man = srs_bdrf['manAnder']
            ander_dienstverband_vrouw = srs_bdrf['vrouwAnder']
            
            totaal_personeel_wsw_dienstverband = wsw_dienstverband_man + wsw_dienstverband_vrouw
            
            totaal_personeel_ander_dienstverband = ander_dienstverband_man + ander_dienstverband_vrouw   
        
            personeel_naar_geslacht_totaal_man = wsw_dienstverband_man + ander_dienstverband_man
            
            personeel_naar_geslacht_totaal_vrouw = wsw_dienstverband_vrouw + ander_dienstverband_vrouw
            
            totaal_personeel_naar_geslacht = personeel_naar_geslacht_totaal_man + personeel_naar_geslacht_totaal_vrouw

            
            calc_verzuimpercentage_totaal = (srs_bdrf['tot_verz_WSW'] * totaal_personeel_wsw_dienstverband + srs_bdrf["tot_verz_Ander"] * totaal_personeel_ander_dienstverband)/totaal_personeel_naar_geslacht
            calc_verzuimpercentage_kwartiel_1 = def_kwartielen_verzuimpercentage(totaal_personeel_naar_geslacht)*100
            calc_verzuimfrequentie_kwartiel_1 = def_kwartielen_verzuimfrequentie(totaal_personeel_naar_geslacht)
        
            calc_gemiddelde_meldfreq_totaal = (srs_bdrf['Tot_gem_meldfreq_WSW1'] * totaal_personeel_wsw_dienstverband + srs_bdrf["Tot_gem_meldfreq_Ander"] * totaal_personeel_ander_dienstverband)/totaal_personeel_naar_geslacht
            
            verzuimpercVenster = def_grootteklasse_verzuimpercentage(totaal_personeel_naar_geslacht)
            verzuimfreqVenster = def_grootteklasse_verzuimfrequentie(totaal_personeel_naar_geslacht)
            
            
            # print(srs_bdrf["_fd_Edit"])            
            # print('verzuimpercVenster:',verzuimpercVenster)            
            # print('verzuimfreqVenster:',verzuimfreqVenster)
            
            data = {
                'Naam' : 
                    [srs_bdrf["_fd_Edit"], "1e Kwartiel"],
                'Verzuimpercentage' : 
                        [calc_verzuimpercentage_totaal, calc_verzuimpercentage_kwartiel_1 ], 
                'Gemiddelde meldingsfrequentie' : 
                    [calc_gemiddelde_meldfreq_totaal, calc_verzuimfrequentie_kwartiel_1 ],
                'label' : [srs_bdrf["_fd_Edit"] + ", " + "{:.1%}".format(calc_verzuimpercentage_totaal/100) + ", " + "{:.2f}".format(calc_gemiddelde_meldfreq_totaal),
                "1e Kwartiel" + ", " + "{:.1%}".format(calc_verzuimpercentage_kwartiel_1/100) + ", " + "{:.2f}".format(calc_verzuimfrequentie_kwartiel_1)],
                'verzuimfreqVenster': verzuimfreqVenster,
                'verzuimpercVenster': verzuimpercVenster
            }
            
            company_list.append(data)
        
        filtered_list = [d for d in company_list if d['Naam'] == ['WVS', '1e Kwartiel']]
        return jsonify(filtered_list[0])
    
    else:
        return (f"Error: {response.status_code}")

#adding a route to the flask server with the url /sum
@app.route("/verzuimpercentage", methods=['GET'])
def verzuimpercentage():
    response = requests.get('http://127.0.0.1:5006/query-data')
    if response.status_code == 200:
        data = response.json()
        
        df_grootteklasse_dict = {}
        df_grootteklasse__list_dict = data['df_grootteklasse']
        for item in df_grootteklasse__list_dict:
            df_grootteklasse_dict[item['Grootteklasse']] = {
                'Verzuimpercentage': item['Verzuimpercentage'],
                'Verzuimduur': item['Verzuimduur'],
                'Meldingsfrequentie': item['Meldingsfrequentie']
            }
            
        df_data= pd.DataFrame.from_dict(data['df_data'])
        df_grootteklasse = pd.DataFrame.from_dict(df_grootteklasse_dict)
        df_grootteklasse = df_grootteklasse.T
        df_grootteklasse = df_grootteklasse.rename_axis("Grootteklasse").reset_index(drop=False)
        df_quartiles_verzuimpercentage = pd.DataFrame.from_dict(data['df_quartiles_verzuimpercentage'])
        df_quartiles_verzuimfrequentie = pd.DataFrame.from_dict(data['df_quartiles_verzuimfrequentie'])
        
        # Benchmark Dataframe
        list_verzuim_wsw = []
        list_verzuim_ander = []
        list_verzuim_PW = []
        list_verzuim_wsw_naar_leeftijd_25 = []
        list_verzuim_wsw_naar_leeftijd_25_34 = []
        list_verzuim_wsw_naar_leeftijd_35_44 = []
        list_verzuim_wsw_naar_leeftijd_45_54 = []
        list_verzuim_wsw_naar_leeftijd_55 = []
        list_verzuim_ander_naar_leeftijd_25 = []
        list_verzuim_ander_naar_leeftijd_25_34 = []
        list_verzuim_ander_naar_leeftijd_35_44 = []
        list_verzuim_ander_naar_leeftijd_45_54 = []
        list_verzuim_ander_naar_leeftijd_55 = []
        list_verzuim_PW_naar_leeftijd_25 = []
        list_verzuim_PW_naar_leeftijd_25_34 = []
        list_verzuim_PW_naar_leeftijd_35_44 = []
        list_verzuim_PW_naar_leeftijd_45_54 = []
        list_verzuim_PW_naar_leeftijd_55 = []
        list_verzuim_perc_man_wsw = []
        list_verzuim_perc_vrouw_wsw = []
        list_verzuim_perc_man_ander = []
        list_verzuim_perc_vrouw_ander = []
        list_verzuim_perc_man_PW = []
        list_verzuim_perc_vrouw_PW = []
        list_gemiddelde_meldingsfrequentie_wsw = []
        list_gemiddelde_meldingsfrequentie_ander = []
        list_gemiddelde_meldingsfrequentie_PW = []
        list_gemiddelde_verzuimduur_wsw =[]
        list_gemiddelde_verzuimduur_PW =[]
        list_gemiddelde_verzuimduur_ander = []
        list_controle_wsw_verzuim_naar_leeftijd = []
        list_controle_PW_verzuim_naar_leeftijd = []
        list_controle_ander_verzuim_naar_leeftijd = []
        list_controle_wsw_verzuim_naar_geslacht = []
        list_controle_PW_verzuim_naar_geslacht = []
        list_controle_ander_verzuim_naar_geslacht = []
        list_person_wsw = []
        list_person_ander = []
        list_person_PW = []
        list_man_wsw = []
        list_man_PW = []
        list_vrouw_wsw = []
        list_man_ander = []
        list_vrouw_ander = []
        list_vrouw_PW = []

        for bedrijf in df_data.index:
            ### Verzuim WSW # Column 1
            srs_bdrf = df_data.iloc[bedrijf]

            list_person_wsw.append(srs_bdrf['Person_WSW'])
            list_person_ander.append(srs_bdrf['Person_ander'])
            list_person_PW.append(srs_bdrf['Person_PW'])

            list_man_wsw.append(srs_bdrf['manWSW'])
            list_vrouw_wsw.append(srs_bdrf['vrouwWSW'])
            list_man_ander.append(srs_bdrf['manAnder'])
            list_vrouw_ander.append(srs_bdrf['vrouwAnder'])

            list_man_PW.append(srs_bdrf['manPW'])
            list_vrouw_PW.append(srs_bdrf['vrouwPW'])
            
            calc_verzuim_wsw = (srs_bdrf['tot_verz_WSW']/100)*srs_bdrf['Person_WSW']
            list_verzuim_wsw.append(calc_verzuim_wsw)

            ### Verzuim Ander # Column 2
            calc_verzuim_ander = srs_bdrf['Person_ander']*(srs_bdrf['tot_verz_Ander']/100)
            list_verzuim_ander.append(calc_verzuim_ander)

            ### Verzuim PW
            calc_verzuim_PW = srs_bdrf['Person_PW']*(srs_bdrf['tot_verz_PW']/100)
            list_verzuim_PW.append(calc_verzuim_PW)

            ### Verzuim WSW naar leeftijd 25
            calc_verzuim_wsw_naar_leeftijd_25 = (srs_bdrf['Verz_WSW25']/100)*srs_bdrf['WSW25']
            list_verzuim_wsw_naar_leeftijd_25.append(calc_verzuim_wsw_naar_leeftijd_25)

            ### Verzuim WSW naar leeftijd 25-34
            calc_verzuim_wsw_naar_leeftijd_25_34 = (srs_bdrf['Verz_WSW25_34']/100)*srs_bdrf['WSW25_34']
            list_verzuim_wsw_naar_leeftijd_25_34.append(calc_verzuim_wsw_naar_leeftijd_25_34)

            ### Verzuim WSW naar leeftijd 35-44
            calc_verzuim_wsw_naar_leeftijd_35_44 = (srs_bdrf['Verz_WSW35_44']/100)*srs_bdrf['WSW35_44']
            list_verzuim_wsw_naar_leeftijd_35_44.append(calc_verzuim_wsw_naar_leeftijd_35_44)

            ### Verzuim WSW naar leeftijd 45-54
            calc_verzuim_wsw_naar_leeftijd_45_54 = (srs_bdrf['Verz_WSW45_54']/100)*srs_bdrf['WSW45_54']
            list_verzuim_wsw_naar_leeftijd_45_54.append(calc_verzuim_wsw_naar_leeftijd_45_54)

            ### Verzuim WSW naar leeftijd 55
            calc_verzuim_wsw_naar_leeftijd_55 = (srs_bdrf['Verz_WSW55']/100)*srs_bdrf['WSW55']
            list_verzuim_wsw_naar_leeftijd_55.append(calc_verzuim_wsw_naar_leeftijd_55)

            ### Verzuim PW naar leeftijd 25
            calc_verzuim_PW_naar_leeftijd_25 = (srs_bdrf['Verz_PW25']/100)*srs_bdrf['PW25']
            list_verzuim_PW_naar_leeftijd_25.append(calc_verzuim_PW_naar_leeftijd_25)

            ### Verzuim PW naar leeftijd 25-34
            calc_verzuim_PW_naar_leeftijd_25_34 = (srs_bdrf['Verz_PW25_34']/100)*srs_bdrf['PW25_34']
            list_verzuim_PW_naar_leeftijd_25_34.append(calc_verzuim_PW_naar_leeftijd_25_34)

            ### Verzuim PW naar leeftijd 35-44
            calc_verzuim_PW_naar_leeftijd_35_44 = (srs_bdrf['Verz_PW35_44']/100)*srs_bdrf['PW35_44']
            list_verzuim_PW_naar_leeftijd_35_44.append(calc_verzuim_PW_naar_leeftijd_35_44)

            ### Verzuim PW naar leeftijd 45-54
            calc_verzuim_PW_naar_leeftijd_45_54 = (srs_bdrf['Verz_PW45_54']/100)*srs_bdrf['PW45_54']
            list_verzuim_PW_naar_leeftijd_45_54.append(calc_verzuim_PW_naar_leeftijd_45_54)

            ### Verzuim PW naar leeftijd 55
            calc_verzuim_PW_naar_leeftijd_55 = (srs_bdrf['Verz_PW55']/100)*srs_bdrf['PW55']
            list_verzuim_PW_naar_leeftijd_55.append(calc_verzuim_PW_naar_leeftijd_55)

            ### Verzuim Ander naar leeftijd 25
            calc_verzuim_ander_naar_leeftijd_25 = (srs_bdrf['Verz_Ander25']/100)*srs_bdrf['Ander25']
            list_verzuim_ander_naar_leeftijd_25.append(calc_verzuim_ander_naar_leeftijd_25)

            ### Verzuim Ander naar leeftijd 25-34
            calc_verzuim_ander_naar_leeftijd_25_34 = (srs_bdrf['Verz_Ander25_34']/100)*srs_bdrf['Ander25_34']
            list_verzuim_ander_naar_leeftijd_25_34.append(calc_verzuim_ander_naar_leeftijd_25_34)

            ### Verzuim Ander naar leeftijd 35-44
            calc_verzuim_ander_naar_leeftijd_35_44 = (srs_bdrf['Verz_Ander35_44']/100)*srs_bdrf['Ander35_44']
            list_verzuim_ander_naar_leeftijd_35_44.append(calc_verzuim_ander_naar_leeftijd_35_44)

            ### Verzuim Ander naar leeftijd 45-54
            calc_verzuim_ander_naar_leeftijd_45_54 = (srs_bdrf['Verz_Ander45_54']/100)*srs_bdrf['Ander45_54']
            list_verzuim_ander_naar_leeftijd_45_54.append(calc_verzuim_ander_naar_leeftijd_45_54)

            ### Verzuim Ander naar leeftijd 45-54
            calc_verzuim_ander_naar_leeftijd_55 = (srs_bdrf['Verz_Ander55']/100)*srs_bdrf['Ander55']
            list_verzuim_ander_naar_leeftijd_55.append(calc_verzuim_ander_naar_leeftijd_55)

            ### Verzuim percentage man WSW
            calc_verzuim_perc_man_wsw = (srs_bdrf['Verz_man_WSW']/100)*srs_bdrf['manWSW']
            list_verzuim_perc_man_wsw.append(calc_verzuim_perc_man_wsw)

            ### Verzuim percentage vrouw WSW
            calc_verzuim_perc_vrouw_wsw = (srs_bdrf['Verz_vrouw_WSW']/100)*srs_bdrf['vrouwWSW']
            list_verzuim_perc_vrouw_wsw.append(calc_verzuim_perc_vrouw_wsw)

            ### Verzuim percentage man Ander
            calc_verzuim_perc_man_ander = (srs_bdrf['Verz_man_Ander']/100)*srs_bdrf['manAnder']
            list_verzuim_perc_man_ander.append(calc_verzuim_perc_man_ander)

            ### Verzuim percentage vrouw Ander
            calc_verzuim_perc_vrouw_ander = (srs_bdrf['Verz_vrouw_Ander']/100)*srs_bdrf['vrouwAnder']
            list_verzuim_perc_vrouw_ander.append(calc_verzuim_perc_vrouw_ander)

            ### Verzuim percentage man PW
            calc_verzuim_perc_man_PW = (srs_bdrf['Verz_man_PW']/100)*srs_bdrf['manPW']
            list_verzuim_perc_man_PW.append(calc_verzuim_perc_man_PW)

            ### Verzuim percentage vrouw PW
            calc_verzuim_perc_vrouw_PW = (srs_bdrf['Verz_vrouw_PW']/100)*srs_bdrf['vrouwPW']
            list_verzuim_perc_vrouw_PW.append(calc_verzuim_perc_vrouw_PW)

            ### Gemiddelde meldingsfrequentie WSW
            calc_gemiddelde_meldingsfrequentie_wsw = srs_bdrf['Tot_gem_meldfreq_WSW1']*srs_bdrf['Person_WSW']
            list_gemiddelde_meldingsfrequentie_wsw.append(calc_gemiddelde_meldingsfrequentie_wsw)

            ### Gemiddelde meldingsfrequentie Ander
            calc_gemiddelde_meldingsfrequentie_ander = srs_bdrf['Tot_gem_meldfreq_Ander']*srs_bdrf['Person_ander']
            list_gemiddelde_meldingsfrequentie_ander.append(calc_gemiddelde_meldingsfrequentie_ander)

            ### Gemiddelde meldingsfrequentie PW
            calc_gemiddelde_meldingsfrequentie_PW = srs_bdrf['Tot_gem_meldfreq_PW']*srs_bdrf['Person_PW']
            list_gemiddelde_meldingsfrequentie_PW.append(calc_gemiddelde_meldingsfrequentie_PW)

            ### Gemiddelde verzuimduur WSW
            calc_gemiddelde_verzuimduur_wsw = srs_bdrf['Gem_verzd_WSW']*srs_bdrf['Person_WSW']
            list_gemiddelde_verzuimduur_wsw.append(calc_gemiddelde_verzuimduur_wsw)

            ### Gemiddelde verzuimduur PW
            calc_gemiddelde_verzuimduur_PW = srs_bdrf['Gem_verzd_PW']*srs_bdrf['Person_PW']
            list_gemiddelde_verzuimduur_PW.append(calc_gemiddelde_verzuimduur_PW)
            
            ### Gemiddelde verzuimduur Ander
            calc_gemiddelde_verzuimduur_ander = srs_bdrf['Gem_verzd_Ander']*srs_bdrf['Person_ander']
            list_gemiddelde_verzuimduur_ander.append(calc_gemiddelde_verzuimduur_ander)

            ### Controle WSW verzuim naar leeftijd
            calc_controle_wsw_verzuim_naar_leeftijd = calc_verzuim_wsw - (calc_verzuim_wsw_naar_leeftijd_25 + calc_verzuim_wsw_naar_leeftijd_25_34 
                + calc_verzuim_wsw_naar_leeftijd_35_44 + calc_verzuim_wsw_naar_leeftijd_45_54 + calc_verzuim_wsw_naar_leeftijd_55)
            list_controle_wsw_verzuim_naar_leeftijd.append(calc_controle_wsw_verzuim_naar_leeftijd)

            ### Controle PW verzuim naar leeftijd
            calc_controle_PW_verzuim_naar_leeftijd = calc_verzuim_PW - (calc_verzuim_PW_naar_leeftijd_25 + calc_verzuim_PW_naar_leeftijd_25_34 
                + calc_verzuim_PW_naar_leeftijd_35_44 + calc_verzuim_PW_naar_leeftijd_45_54 + calc_verzuim_PW_naar_leeftijd_55)
            list_controle_PW_verzuim_naar_leeftijd.append(calc_controle_PW_verzuim_naar_leeftijd)

            ### Controle Ander verzuim naar leeftijd
            calc_controle_ander_verzuim_naar_leeftijd = calc_verzuim_ander - (calc_verzuim_ander_naar_leeftijd_25 + calc_verzuim_ander_naar_leeftijd_25_34 
                + calc_verzuim_ander_naar_leeftijd_35_44 + calc_verzuim_ander_naar_leeftijd_45_54 + calc_verzuim_ander_naar_leeftijd_55)
            list_controle_ander_verzuim_naar_leeftijd.append(calc_controle_ander_verzuim_naar_leeftijd)

            ### Controle WSW verzuim naar geslacht
            calc_controle_wsw_verzuim_naar_geslacht = calc_verzuim_wsw - calc_verzuim_perc_man_wsw - calc_verzuim_perc_vrouw_wsw
            list_controle_wsw_verzuim_naar_geslacht.append(calc_controle_wsw_verzuim_naar_geslacht)

            ### Controle PW verzuim naar geslacht
            calc_controle_PW_verzuim_naar_geslacht = calc_verzuim_PW - calc_verzuim_perc_man_PW - calc_verzuim_perc_vrouw_PW
            list_controle_PW_verzuim_naar_geslacht.append(calc_controle_PW_verzuim_naar_geslacht)

            ### Controle Ander verzuim naar geslacht
            calc_controle_ander_verzuim_naar_geslacht = calc_verzuim_ander - calc_verzuim_perc_man_ander - calc_verzuim_perc_vrouw_ander
            list_controle_ander_verzuim_naar_geslacht.append(calc_controle_ander_verzuim_naar_geslacht)

        #Replace nan with ""
        list_verzuim_wsw = [0 if math.isnan(x) else x for x in list_verzuim_wsw]
        list_verzuim_PW = [0 if math.isnan(x) else x for x in list_verzuim_PW]
        list_verzuim_ander = [0 if math.isnan(x) else x for x in list_verzuim_ander]
        list_verzuim_wsw_naar_leeftijd_25 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_25]
        list_verzuim_wsw_naar_leeftijd_25_34 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_25_34]
        list_verzuim_wsw_naar_leeftijd_35_44 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_35_44]
        list_verzuim_wsw_naar_leeftijd_45_54 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_45_54]
        list_verzuim_wsw_naar_leeftijd_55 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_55]
        list_verzuim_PW_naar_leeftijd_25 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_25]
        list_verzuim_PW_naar_leeftijd_25_34 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_25_34]
        list_verzuim_PW_naar_leeftijd_35_44 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_35_44]
        list_verzuim_PW_naar_leeftijd_45_54 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_45_54]
        list_verzuim_PW_naar_leeftijd_55 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_55]
        list_verzuim_ander_naar_leeftijd_25 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_25]
        list_verzuim_ander_naar_leeftijd_25_34 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_25_34]
        list_verzuim_ander_naar_leeftijd_35_44 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_35_44]
        list_verzuim_ander_naar_leeftijd_45_54 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_45_54]
        list_verzuim_ander_naar_leeftijd_55 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_55]
        list_verzuim_perc_man_wsw = [0 if math.isnan(x) else x for x in list_verzuim_perc_man_wsw]
        list_verzuim_perc_vrouw_wsw = [0 if math.isnan(x) else x for x in list_verzuim_perc_vrouw_wsw]
        list_verzuim_perc_man_PW = [0 if math.isnan(x) else x for x in list_verzuim_perc_man_PW]
        list_verzuim_perc_vrouw_PW = [0 if math.isnan(x) else x for x in list_verzuim_perc_vrouw_PW]
        list_verzuim_perc_man_ander = [0 if math.isnan(x) else x for x in list_verzuim_perc_man_ander]
        list_verzuim_perc_vrouw_ander = [0 if math.isnan(x) else x for x in list_verzuim_perc_vrouw_ander]
        list_gemiddelde_meldingsfrequentie_wsw = [0 if math.isnan(x) else x for x in list_gemiddelde_meldingsfrequentie_wsw]
        list_gemiddelde_meldingsfrequentie_PW = [0 if math.isnan(x) else x for x in list_gemiddelde_meldingsfrequentie_PW]
        list_gemiddelde_meldingsfrequentie_ander = [0 if math.isnan(x) else x for x in list_gemiddelde_meldingsfrequentie_ander]
        list_gemiddelde_verzuimduur_wsw = [0 if math.isnan(x) else x for x in list_gemiddelde_verzuimduur_wsw]
        list_gemiddelde_verzuimduur_PW = [0 if math.isnan(x) else x for x in list_gemiddelde_verzuimduur_PW]
        list_gemiddelde_verzuimduur_ander = [0 if math.isnan(x) else x for x in list_gemiddelde_verzuimduur_ander]
        list_controle_wsw_verzuim_naar_leeftijd = [0 if math.isnan(x) else x for x in list_controle_wsw_verzuim_naar_leeftijd]
        list_controle_PW_verzuim_naar_leeftijd = [0 if math.isnan(x) else x for x in list_controle_PW_verzuim_naar_leeftijd]
        list_controle_ander_verzuim_naar_leeftijd = [0 if math.isnan(x) else x for x in list_controle_ander_verzuim_naar_leeftijd]
        list_controle_wsw_verzuim_naar_geslacht = [0 if math.isnan(x) else x for x in list_controle_wsw_verzuim_naar_geslacht]
        list_controle_PW_verzuim_naar_geslacht = [0 if math.isnan(x) else x for x in list_controle_PW_verzuim_naar_geslacht]
        list_controle_ander_verzuim_naar_geslacht = [0 if math.isnan(x) else x for x in list_controle_ander_verzuim_naar_geslacht]
        list_person_wsw = [0 if math.isnan(x) else x for x in list_person_wsw]
        list_person_PW = [0 if math.isnan(x) else x for x in list_person_PW]
        list_person_ander = [0 if math.isnan(x) else x for x in list_person_ander]
        list_man_wsw = [0 if math.isnan(x) else x for x in list_man_wsw]
        list_vrouw_wsw = [0 if math.isnan(x) else x for x in list_vrouw_wsw]
        list_man_PW = [0 if math.isnan(x) else x for x in list_man_PW]
        list_vrouw_PW = [0 if math.isnan(x) else x for x in list_vrouw_PW]
        list_man_ander = [0 if math.isnan(x) else x for x in list_man_ander]
        list_vrouw_ander = [0 if math.isnan(x) else x for x in list_vrouw_ander]

        benchmark_data = {
            'Verzuim WSW': list_verzuim_wsw,
            'Verzuim PW': list_verzuim_PW,
            'Verzuim Ander': list_verzuim_ander,
            'Verzuim WSW naar leeftijd 25': list_verzuim_wsw_naar_leeftijd_25,
            'Verzuim WSW naar leeftijd 25-34': list_verzuim_wsw_naar_leeftijd_25_34,
            'Verzuim WSW naar leeftijd 35-44': list_verzuim_wsw_naar_leeftijd_35_44,
            'Verzuim WSW naar leeftijd 45-54':list_verzuim_wsw_naar_leeftijd_45_54,
            'Verzuim WSW naar leeftijd 55':list_verzuim_wsw_naar_leeftijd_55,
            'Verzuim PW naar leeftijd 25': list_verzuim_PW_naar_leeftijd_25,
            'Verzuim PW naar leeftijd 25-34': list_verzuim_PW_naar_leeftijd_25_34,
            'Verzuim PW naar leeftijd 35-44': list_verzuim_PW_naar_leeftijd_35_44,
            'Verzuim PW naar leeftijd 45-54':list_verzuim_PW_naar_leeftijd_45_54,
            'Verzuim PW naar leeftijd 55':list_verzuim_PW_naar_leeftijd_55,
            'Verzuim Ander naar leeftijd 25': list_verzuim_ander_naar_leeftijd_25,
            'Verzuim Ander naar leeftijd 25-34': list_verzuim_ander_naar_leeftijd_25_34,
            'Verzuim Ander naar leeftijd 35-44': list_verzuim_ander_naar_leeftijd_35_44,
            'Verzuim Ander naar leeftijd 45-54': list_verzuim_ander_naar_leeftijd_45_54,
            'Verzuim Ander naar leeftijd 55': list_verzuim_ander_naar_leeftijd_55,
            'Verzuim percentage man WSW': list_verzuim_perc_man_wsw,
            'Verzuim percentage vrouw WSW': list_verzuim_perc_vrouw_wsw,
            'Verzuim percentage man PW': list_verzuim_perc_man_PW,
            'Verzuim percentage vrouw PW': list_verzuim_perc_vrouw_PW,
            'Verzuim percentage man Ander': list_verzuim_perc_man_ander,
            'Verzuim percentage vrouw Ander': list_verzuim_perc_vrouw_ander,
            'Gemiddelde meldingsfrequentie WSW': list_gemiddelde_meldingsfrequentie_wsw,
            'Gemiddelde meldingsfrequentie PW': list_gemiddelde_meldingsfrequentie_PW,
            'Gemiddelde meldingsfrequentie Ander': list_gemiddelde_meldingsfrequentie_ander,
            'Gemiddelde verzuimduur WSW': list_gemiddelde_verzuimduur_wsw,
            'Gemiddelde verzuimduur PW': list_gemiddelde_verzuimduur_PW,
            'Gemiddelde verzuimduur Ander': list_gemiddelde_verzuimduur_ander,
            'Controle WSW verzuim naar leeftijd': list_controle_wsw_verzuim_naar_leeftijd,
            'Controle PW verzuim naar leeftijd': list_controle_PW_verzuim_naar_leeftijd,
            'Controle Ander verzuim naar leeftijd': list_controle_ander_verzuim_naar_leeftijd,
            'Controle WSW verzuim naar geslacht': list_controle_wsw_verzuim_naar_geslacht,
            'Controle PW verzuim naar geslacht': list_controle_PW_verzuim_naar_geslacht,
            'Controle Ander verzuim naar geslacht': list_controle_ander_verzuim_naar_geslacht
        }
        
        gemiddelde_verzuimduur_wsw_dienstverband = sum(list_gemiddelde_verzuimduur_wsw)/sum(list_person_wsw)
        gemiddelde_verzuimduur_PW_dienstverband = sum(list_gemiddelde_verzuimduur_PW)/sum(list_person_PW)
        gemiddelde_verzuimduur_ander_dienstverband = sum(list_gemiddelde_verzuimduur_ander)/sum(list_person_ander)

        totaal_personeel_naar_geslacht_wsw_dienstverband = sum(list_man_wsw) + sum(list_vrouw_wsw)
        totaal_personeel_naar_geslacht_Ander_dienstverband = sum(list_man_ander) + sum(list_vrouw_ander)
        totaal_personeel_naar_geslacht_PW_dienstverband = sum(list_man_PW) + sum(list_vrouw_PW)
        totaal_personeel_naar_geslacht_totaal = (sum(list_man_wsw) + sum(list_man_ander)) + + sum(list_man_PW)+ sum(list_vrouw_PW)+ (sum(list_vrouw_wsw) + sum(list_vrouw_ander))

        bm_gemiddelde_verzuimduur_totaal = (gemiddelde_verzuimduur_wsw_dienstverband*totaal_personeel_naar_geslacht_wsw_dienstverband
                                            + gemiddelde_verzuimduur_PW_dienstverband*totaal_personeel_naar_geslacht_PW_dienstverband
                                            + gemiddelde_verzuimduur_ander_dienstverband*totaal_personeel_naar_geslacht_Ander_dienstverband)/totaal_personeel_naar_geslacht_totaal
        
        ##### Grafiek 1: verzuimpercentage #####
        from tkinter import font


        for bedrijf in df_data.index:
            ### Define Series
            srs_bdrf = df_data.iloc[bedrijf]

            wsw_dienstverband_man = srs_bdrf['manWSW']
            wsw_dienstverband_vrouw = srs_bdrf['vrouwWSW']
            PW_dienstverband_man = srs_bdrf['manPW']
            PW_dienstverband_vrouw = srs_bdrf['vrouwPW']
            ander_dienstverband_man = srs_bdrf['manAnder']
            ander_dienstverband_vrouw = srs_bdrf['vrouwAnder']
            personeel_naar_geslacht_totaal_man = wsw_dienstverband_man + ander_dienstverband_man + PW_dienstverband_man
            personeel_naar_geslacht_totaal_vrouw = wsw_dienstverband_vrouw + ander_dienstverband_vrouw + PW_dienstverband_vrouw
            totaal_personeel_wsw_dienstverband = wsw_dienstverband_man + wsw_dienstverband_vrouw
            totaal_personeel_PW_dienstverband = PW_dienstverband_man + PW_dienstverband_vrouw
            totaal_personeel_ander_dienstverband = ander_dienstverband_man + ander_dienstverband_vrouw
            totaal_personeel_naar_geslacht = personeel_naar_geslacht_totaal_man + personeel_naar_geslacht_totaal_vrouw
            gemiddelde_verzuimduur_totaal = ((srs_bdrf["Gem_verzd_WSW"] * totaal_personeel_wsw_dienstverband + 
                                                srs_bdrf["Gem_verzd_PW"] * totaal_personeel_PW_dienstverband +
                                                srs_bdrf["Gem_verzd_Ander"]* totaal_personeel_ander_dienstverband)/totaal_personeel_naar_geslacht)
            

            ### verzuimpercentage wsw-dienstverband // TOEVOEGEN PW IN GEWOGEN GEMIDDELDE
            calc_verzuimpercentage_totaal = (srs_bdrf['tot_verz_WSW'] * totaal_personeel_wsw_dienstverband + srs_bdrf['tot_verz_PW'] * totaal_personeel_PW_dienstverband + srs_bdrf["tot_verz_Ander"] * totaal_personeel_ander_dienstverband)/totaal_personeel_naar_geslacht
            verzuimpercentage_wsw_dienstverband = sum(list_verzuim_wsw)/sum(list_person_wsw)
            verzuimpercentage_PW_dienstverband = sum(list_verzuim_PW)/sum(list_person_PW)
            verzuimpercentage_ander_dienstverband = sum(list_verzuim_ander)/sum(list_person_ander)
            

            ### verzuimpercentage BM //TOEVOEGEN PW
            calc_bm_verzuimpercentage = ((verzuimpercentage_wsw_dienstverband * totaal_personeel_naar_geslacht_wsw_dienstverband + 
                                                verzuimpercentage_PW_dienstverband * totaal_personeel_naar_geslacht_PW_dienstverband + 
                                                verzuimpercentage_ander_dienstverband * totaal_personeel_naar_geslacht_Ander_dienstverband) / totaal_personeel_naar_geslacht_totaal)
            ### Data
            data = {'Type Dienstverband' : 
                        ['Wsw', 'PW','Overige', 'Totaal', "Benchmark", "Wsw", 'PW',"Overige", "Totaal", "Benchmark"], 
                'Jaar' : 
                        ["2021", "2021", "2021", "2021", "2021","2022","2022", "2022", "2022", "2022"], 
                'Verzuimpercentage' : 
                    [srs_bdrf["VerzuimpercentageWSW2021"], 0,srs_bdrf["VerzuimpercentageOverige2021"], srs_bdrf["VerzuimpercentageTotaal2021"], srs_bdrf["BMVerzuimpercentageTotaal2021"], 
                    srs_bdrf['tot_verz_WSW']/100, srs_bdrf['tot_verz_PW']/100,srs_bdrf["tot_verz_Ander"]/100, calc_verzuimpercentage_totaal/100, calc_bm_verzuimpercentage]}
        
        return jsonify(data)


#adding a route to the flask server with the url /sum
@app.route("/verzuimpercentagegeslacht", methods=['GET'])
def verzuimpercentagegeslacht():
    
    response = requests.get('http://127.0.0.1:5006/query-data')
    if response.status_code == 200:
        data = response.json()
        
        df_grootteklasse_dict = {}
        df_grootteklasse__list_dict = data['df_grootteklasse']
        for item in df_grootteklasse__list_dict:
            df_grootteklasse_dict[item['Grootteklasse']] = {
                'Verzuimpercentage': item['Verzuimpercentage'],
                'Verzuimduur': item['Verzuimduur'],
                'Meldingsfrequentie': item['Meldingsfrequentie']
            }
            
        df_data= pd.DataFrame.from_dict(data['df_data'])
        df_grootteklasse = pd.DataFrame.from_dict(df_grootteklasse_dict)
        df_grootteklasse = df_grootteklasse.T
        df_grootteklasse = df_grootteklasse.rename_axis("Grootteklasse").reset_index(drop=False)
        df_quartiles_verzuimpercentage = pd.DataFrame.from_dict(data['df_quartiles_verzuimpercentage'])
        df_quartiles_verzuimfrequentie = pd.DataFrame.from_dict(data['df_quartiles_verzuimfrequentie'])
        
        # Benchmark Dataframe
        list_verzuim_wsw = []
        list_verzuim_ander = []
        list_verzuim_PW = []
        list_verzuim_wsw_naar_leeftijd_25 = []
        list_verzuim_wsw_naar_leeftijd_25_34 = []
        list_verzuim_wsw_naar_leeftijd_35_44 = []
        list_verzuim_wsw_naar_leeftijd_45_54 = []
        list_verzuim_wsw_naar_leeftijd_55 = []
        list_verzuim_ander_naar_leeftijd_25 = []
        list_verzuim_ander_naar_leeftijd_25_34 = []
        list_verzuim_ander_naar_leeftijd_35_44 = []
        list_verzuim_ander_naar_leeftijd_45_54 = []
        list_verzuim_ander_naar_leeftijd_55 = []
        list_verzuim_PW_naar_leeftijd_25 = []
        list_verzuim_PW_naar_leeftijd_25_34 = []
        list_verzuim_PW_naar_leeftijd_35_44 = []
        list_verzuim_PW_naar_leeftijd_45_54 = []
        list_verzuim_PW_naar_leeftijd_55 = []
        list_verzuim_perc_man_wsw = []
        list_verzuim_perc_vrouw_wsw = []
        list_verzuim_perc_man_ander = []
        list_verzuim_perc_vrouw_ander = []
        list_verzuim_perc_man_PW = []
        list_verzuim_perc_vrouw_PW = []
        list_gemiddelde_meldingsfrequentie_wsw = []
        list_gemiddelde_meldingsfrequentie_ander = []
        list_gemiddelde_meldingsfrequentie_PW = []
        list_gemiddelde_verzuimduur_wsw =[]
        list_gemiddelde_verzuimduur_PW =[]
        list_gemiddelde_verzuimduur_ander = []
        list_controle_wsw_verzuim_naar_leeftijd = []
        list_controle_PW_verzuim_naar_leeftijd = []
        list_controle_ander_verzuim_naar_leeftijd = []
        list_controle_wsw_verzuim_naar_geslacht = []
        list_controle_PW_verzuim_naar_geslacht = []
        list_controle_ander_verzuim_naar_geslacht = []
        list_person_wsw = []
        list_person_ander = []
        list_person_PW = []
        list_man_wsw = []
        list_man_PW = []
        list_vrouw_wsw = []
        list_man_ander = []
        list_vrouw_ander = []
        list_vrouw_PW = []

        for bedrijf in df_data.index:
            ### Verzuim WSW # Column 1
            srs_bdrf = df_data.iloc[bedrijf]

            list_person_wsw.append(srs_bdrf['Person_WSW'])
            list_person_ander.append(srs_bdrf['Person_ander'])
            list_person_PW.append(srs_bdrf['Person_PW'])

            list_man_wsw.append(srs_bdrf['manWSW'])
            list_vrouw_wsw.append(srs_bdrf['vrouwWSW'])
            list_man_ander.append(srs_bdrf['manAnder'])
            list_vrouw_ander.append(srs_bdrf['vrouwAnder'])

            list_man_PW.append(srs_bdrf['manPW'])
            list_vrouw_PW.append(srs_bdrf['vrouwPW'])
            
            calc_verzuim_wsw = (srs_bdrf['tot_verz_WSW']/100)*srs_bdrf['Person_WSW']
            list_verzuim_wsw.append(calc_verzuim_wsw)

            ### Verzuim Ander # Column 2
            calc_verzuim_ander = srs_bdrf['Person_ander']*(srs_bdrf['tot_verz_Ander']/100)
            list_verzuim_ander.append(calc_verzuim_ander)

            ### Verzuim PW
            calc_verzuim_PW = srs_bdrf['Person_PW']*(srs_bdrf['tot_verz_PW']/100)
            list_verzuim_PW.append(calc_verzuim_PW)

            ### Verzuim WSW naar leeftijd 25
            calc_verzuim_wsw_naar_leeftijd_25 = (srs_bdrf['Verz_WSW25']/100)*srs_bdrf['WSW25']
            list_verzuim_wsw_naar_leeftijd_25.append(calc_verzuim_wsw_naar_leeftijd_25)

            ### Verzuim WSW naar leeftijd 25-34
            calc_verzuim_wsw_naar_leeftijd_25_34 = (srs_bdrf['Verz_WSW25_34']/100)*srs_bdrf['WSW25_34']
            list_verzuim_wsw_naar_leeftijd_25_34.append(calc_verzuim_wsw_naar_leeftijd_25_34)

            ### Verzuim WSW naar leeftijd 35-44
            calc_verzuim_wsw_naar_leeftijd_35_44 = (srs_bdrf['Verz_WSW35_44']/100)*srs_bdrf['WSW35_44']
            list_verzuim_wsw_naar_leeftijd_35_44.append(calc_verzuim_wsw_naar_leeftijd_35_44)

            ### Verzuim WSW naar leeftijd 45-54
            calc_verzuim_wsw_naar_leeftijd_45_54 = (srs_bdrf['Verz_WSW45_54']/100)*srs_bdrf['WSW45_54']
            list_verzuim_wsw_naar_leeftijd_45_54.append(calc_verzuim_wsw_naar_leeftijd_45_54)

            ### Verzuim WSW naar leeftijd 55
            calc_verzuim_wsw_naar_leeftijd_55 = (srs_bdrf['Verz_WSW55']/100)*srs_bdrf['WSW55']
            list_verzuim_wsw_naar_leeftijd_55.append(calc_verzuim_wsw_naar_leeftijd_55)

            ### Verzuim PW naar leeftijd 25
            calc_verzuim_PW_naar_leeftijd_25 = (srs_bdrf['Verz_PW25']/100)*srs_bdrf['PW25']
            list_verzuim_PW_naar_leeftijd_25.append(calc_verzuim_PW_naar_leeftijd_25)

            ### Verzuim PW naar leeftijd 25-34
            calc_verzuim_PW_naar_leeftijd_25_34 = (srs_bdrf['Verz_PW25_34']/100)*srs_bdrf['PW25_34']
            list_verzuim_PW_naar_leeftijd_25_34.append(calc_verzuim_PW_naar_leeftijd_25_34)

            ### Verzuim PW naar leeftijd 35-44
            calc_verzuim_PW_naar_leeftijd_35_44 = (srs_bdrf['Verz_PW35_44']/100)*srs_bdrf['PW35_44']
            list_verzuim_PW_naar_leeftijd_35_44.append(calc_verzuim_PW_naar_leeftijd_35_44)

            ### Verzuim PW naar leeftijd 45-54
            calc_verzuim_PW_naar_leeftijd_45_54 = (srs_bdrf['Verz_PW45_54']/100)*srs_bdrf['PW45_54']
            list_verzuim_PW_naar_leeftijd_45_54.append(calc_verzuim_PW_naar_leeftijd_45_54)

            ### Verzuim PW naar leeftijd 55
            calc_verzuim_PW_naar_leeftijd_55 = (srs_bdrf['Verz_PW55']/100)*srs_bdrf['PW55']
            list_verzuim_PW_naar_leeftijd_55.append(calc_verzuim_PW_naar_leeftijd_55)

            ### Verzuim Ander naar leeftijd 25
            calc_verzuim_ander_naar_leeftijd_25 = (srs_bdrf['Verz_Ander25']/100)*srs_bdrf['Ander25']
            list_verzuim_ander_naar_leeftijd_25.append(calc_verzuim_ander_naar_leeftijd_25)

            ### Verzuim Ander naar leeftijd 25-34
            calc_verzuim_ander_naar_leeftijd_25_34 = (srs_bdrf['Verz_Ander25_34']/100)*srs_bdrf['Ander25_34']
            list_verzuim_ander_naar_leeftijd_25_34.append(calc_verzuim_ander_naar_leeftijd_25_34)

            ### Verzuim Ander naar leeftijd 35-44
            calc_verzuim_ander_naar_leeftijd_35_44 = (srs_bdrf['Verz_Ander35_44']/100)*srs_bdrf['Ander35_44']
            list_verzuim_ander_naar_leeftijd_35_44.append(calc_verzuim_ander_naar_leeftijd_35_44)

            ### Verzuim Ander naar leeftijd 45-54
            calc_verzuim_ander_naar_leeftijd_45_54 = (srs_bdrf['Verz_Ander45_54']/100)*srs_bdrf['Ander45_54']
            list_verzuim_ander_naar_leeftijd_45_54.append(calc_verzuim_ander_naar_leeftijd_45_54)

            ### Verzuim Ander naar leeftijd 45-54
            calc_verzuim_ander_naar_leeftijd_55 = (srs_bdrf['Verz_Ander55']/100)*srs_bdrf['Ander55']
            list_verzuim_ander_naar_leeftijd_55.append(calc_verzuim_ander_naar_leeftijd_55)

            ### Verzuim percentage man WSW
            calc_verzuim_perc_man_wsw = (srs_bdrf['Verz_man_WSW']/100)*srs_bdrf['manWSW']
            list_verzuim_perc_man_wsw.append(calc_verzuim_perc_man_wsw)

            ### Verzuim percentage vrouw WSW
            calc_verzuim_perc_vrouw_wsw = (srs_bdrf['Verz_vrouw_WSW']/100)*srs_bdrf['vrouwWSW']
            list_verzuim_perc_vrouw_wsw.append(calc_verzuim_perc_vrouw_wsw)

            ### Verzuim percentage man Ander
            calc_verzuim_perc_man_ander = (srs_bdrf['Verz_man_Ander']/100)*srs_bdrf['manAnder']
            list_verzuim_perc_man_ander.append(calc_verzuim_perc_man_ander)

            ### Verzuim percentage vrouw Ander
            calc_verzuim_perc_vrouw_ander = (srs_bdrf['Verz_vrouw_Ander']/100)*srs_bdrf['vrouwAnder']
            list_verzuim_perc_vrouw_ander.append(calc_verzuim_perc_vrouw_ander)

            ### Verzuim percentage man PW
            calc_verzuim_perc_man_PW = (srs_bdrf['Verz_man_PW']/100)*srs_bdrf['manPW']
            list_verzuim_perc_man_PW.append(calc_verzuim_perc_man_PW)

            ### Verzuim percentage vrouw PW
            calc_verzuim_perc_vrouw_PW = (srs_bdrf['Verz_vrouw_PW']/100)*srs_bdrf['vrouwPW']
            list_verzuim_perc_vrouw_PW.append(calc_verzuim_perc_vrouw_PW)

            ### Gemiddelde meldingsfrequentie WSW
            calc_gemiddelde_meldingsfrequentie_wsw = srs_bdrf['Tot_gem_meldfreq_WSW1']*srs_bdrf['Person_WSW']
            list_gemiddelde_meldingsfrequentie_wsw.append(calc_gemiddelde_meldingsfrequentie_wsw)

            ### Gemiddelde meldingsfrequentie Ander
            calc_gemiddelde_meldingsfrequentie_ander = srs_bdrf['Tot_gem_meldfreq_Ander']*srs_bdrf['Person_ander']
            list_gemiddelde_meldingsfrequentie_ander.append(calc_gemiddelde_meldingsfrequentie_ander)

            ### Gemiddelde meldingsfrequentie PW
            calc_gemiddelde_meldingsfrequentie_PW = srs_bdrf['Tot_gem_meldfreq_PW']*srs_bdrf['Person_PW']
            list_gemiddelde_meldingsfrequentie_PW.append(calc_gemiddelde_meldingsfrequentie_PW)

            ### Gemiddelde verzuimduur WSW
            calc_gemiddelde_verzuimduur_wsw = srs_bdrf['Gem_verzd_WSW']*srs_bdrf['Person_WSW']
            list_gemiddelde_verzuimduur_wsw.append(calc_gemiddelde_verzuimduur_wsw)

            ### Gemiddelde verzuimduur PW
            calc_gemiddelde_verzuimduur_PW = srs_bdrf['Gem_verzd_PW']*srs_bdrf['Person_PW']
            list_gemiddelde_verzuimduur_PW.append(calc_gemiddelde_verzuimduur_PW)
            
            ### Gemiddelde verzuimduur Ander
            calc_gemiddelde_verzuimduur_ander = srs_bdrf['Gem_verzd_Ander']*srs_bdrf['Person_ander']
            list_gemiddelde_verzuimduur_ander.append(calc_gemiddelde_verzuimduur_ander)

            ### Controle WSW verzuim naar leeftijd
            calc_controle_wsw_verzuim_naar_leeftijd = calc_verzuim_wsw - (calc_verzuim_wsw_naar_leeftijd_25 + calc_verzuim_wsw_naar_leeftijd_25_34 
                + calc_verzuim_wsw_naar_leeftijd_35_44 + calc_verzuim_wsw_naar_leeftijd_45_54 + calc_verzuim_wsw_naar_leeftijd_55)
            list_controle_wsw_verzuim_naar_leeftijd.append(calc_controle_wsw_verzuim_naar_leeftijd)

            ### Controle PW verzuim naar leeftijd
            calc_controle_PW_verzuim_naar_leeftijd = calc_verzuim_PW - (calc_verzuim_PW_naar_leeftijd_25 + calc_verzuim_PW_naar_leeftijd_25_34 
                + calc_verzuim_PW_naar_leeftijd_35_44 + calc_verzuim_PW_naar_leeftijd_45_54 + calc_verzuim_PW_naar_leeftijd_55)
            list_controle_PW_verzuim_naar_leeftijd.append(calc_controle_PW_verzuim_naar_leeftijd)

            ### Controle Ander verzuim naar leeftijd
            calc_controle_ander_verzuim_naar_leeftijd = calc_verzuim_ander - (calc_verzuim_ander_naar_leeftijd_25 + calc_verzuim_ander_naar_leeftijd_25_34 
                + calc_verzuim_ander_naar_leeftijd_35_44 + calc_verzuim_ander_naar_leeftijd_45_54 + calc_verzuim_ander_naar_leeftijd_55)
            list_controle_ander_verzuim_naar_leeftijd.append(calc_controle_ander_verzuim_naar_leeftijd)

            ### Controle WSW verzuim naar geslacht
            calc_controle_wsw_verzuim_naar_geslacht = calc_verzuim_wsw - calc_verzuim_perc_man_wsw - calc_verzuim_perc_vrouw_wsw
            list_controle_wsw_verzuim_naar_geslacht.append(calc_controle_wsw_verzuim_naar_geslacht)

            ### Controle PW verzuim naar geslacht
            calc_controle_PW_verzuim_naar_geslacht = calc_verzuim_PW - calc_verzuim_perc_man_PW - calc_verzuim_perc_vrouw_PW
            list_controle_PW_verzuim_naar_geslacht.append(calc_controle_PW_verzuim_naar_geslacht)

            ### Controle Ander verzuim naar geslacht
            calc_controle_ander_verzuim_naar_geslacht = calc_verzuim_ander - calc_verzuim_perc_man_ander - calc_verzuim_perc_vrouw_ander
            list_controle_ander_verzuim_naar_geslacht.append(calc_controle_ander_verzuim_naar_geslacht)

        #Replace nan with ""
        list_verzuim_wsw = [0 if math.isnan(x) else x for x in list_verzuim_wsw]
        list_verzuim_PW = [0 if math.isnan(x) else x for x in list_verzuim_PW]
        list_verzuim_ander = [0 if math.isnan(x) else x for x in list_verzuim_ander]
        list_verzuim_wsw_naar_leeftijd_25 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_25]
        list_verzuim_wsw_naar_leeftijd_25_34 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_25_34]
        list_verzuim_wsw_naar_leeftijd_35_44 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_35_44]
        list_verzuim_wsw_naar_leeftijd_45_54 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_45_54]
        list_verzuim_wsw_naar_leeftijd_55 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_55]
        list_verzuim_PW_naar_leeftijd_25 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_25]
        list_verzuim_PW_naar_leeftijd_25_34 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_25_34]
        list_verzuim_PW_naar_leeftijd_35_44 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_35_44]
        list_verzuim_PW_naar_leeftijd_45_54 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_45_54]
        list_verzuim_PW_naar_leeftijd_55 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_55]
        list_verzuim_ander_naar_leeftijd_25 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_25]
        list_verzuim_ander_naar_leeftijd_25_34 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_25_34]
        list_verzuim_ander_naar_leeftijd_35_44 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_35_44]
        list_verzuim_ander_naar_leeftijd_45_54 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_45_54]
        list_verzuim_ander_naar_leeftijd_55 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_55]
        list_verzuim_perc_man_wsw = [0 if math.isnan(x) else x for x in list_verzuim_perc_man_wsw]
        list_verzuim_perc_vrouw_wsw = [0 if math.isnan(x) else x for x in list_verzuim_perc_vrouw_wsw]
        list_verzuim_perc_man_PW = [0 if math.isnan(x) else x for x in list_verzuim_perc_man_PW]
        list_verzuim_perc_vrouw_PW = [0 if math.isnan(x) else x for x in list_verzuim_perc_vrouw_PW]
        list_verzuim_perc_man_ander = [0 if math.isnan(x) else x for x in list_verzuim_perc_man_ander]
        list_verzuim_perc_vrouw_ander = [0 if math.isnan(x) else x for x in list_verzuim_perc_vrouw_ander]
        list_gemiddelde_meldingsfrequentie_wsw = [0 if math.isnan(x) else x for x in list_gemiddelde_meldingsfrequentie_wsw]
        list_gemiddelde_meldingsfrequentie_PW = [0 if math.isnan(x) else x for x in list_gemiddelde_meldingsfrequentie_PW]
        list_gemiddelde_meldingsfrequentie_ander = [0 if math.isnan(x) else x for x in list_gemiddelde_meldingsfrequentie_ander]
        list_gemiddelde_verzuimduur_wsw = [0 if math.isnan(x) else x for x in list_gemiddelde_verzuimduur_wsw]
        list_gemiddelde_verzuimduur_PW = [0 if math.isnan(x) else x for x in list_gemiddelde_verzuimduur_PW]
        list_gemiddelde_verzuimduur_ander = [0 if math.isnan(x) else x for x in list_gemiddelde_verzuimduur_ander]
        list_controle_wsw_verzuim_naar_leeftijd = [0 if math.isnan(x) else x for x in list_controle_wsw_verzuim_naar_leeftijd]
        list_controle_PW_verzuim_naar_leeftijd = [0 if math.isnan(x) else x for x in list_controle_PW_verzuim_naar_leeftijd]
        list_controle_ander_verzuim_naar_leeftijd = [0 if math.isnan(x) else x for x in list_controle_ander_verzuim_naar_leeftijd]
        list_controle_wsw_verzuim_naar_geslacht = [0 if math.isnan(x) else x for x in list_controle_wsw_verzuim_naar_geslacht]
        list_controle_PW_verzuim_naar_geslacht = [0 if math.isnan(x) else x for x in list_controle_PW_verzuim_naar_geslacht]
        list_controle_ander_verzuim_naar_geslacht = [0 if math.isnan(x) else x for x in list_controle_ander_verzuim_naar_geslacht]
        list_person_wsw = [0 if math.isnan(x) else x for x in list_person_wsw]
        list_person_PW = [0 if math.isnan(x) else x for x in list_person_PW]
        list_person_ander = [0 if math.isnan(x) else x for x in list_person_ander]
        list_man_wsw = [0 if math.isnan(x) else x for x in list_man_wsw]
        list_vrouw_wsw = [0 if math.isnan(x) else x for x in list_vrouw_wsw]
        list_man_PW = [0 if math.isnan(x) else x for x in list_man_PW]
        list_vrouw_PW = [0 if math.isnan(x) else x for x in list_vrouw_PW]
        list_man_ander = [0 if math.isnan(x) else x for x in list_man_ander]
        list_vrouw_ander = [0 if math.isnan(x) else x for x in list_vrouw_ander]

        benchmark_data = {
            'Verzuim WSW': list_verzuim_wsw,
            'Verzuim PW': list_verzuim_PW,
            'Verzuim Ander': list_verzuim_ander,
            'Verzuim WSW naar leeftijd 25': list_verzuim_wsw_naar_leeftijd_25,
            'Verzuim WSW naar leeftijd 25-34': list_verzuim_wsw_naar_leeftijd_25_34,
            'Verzuim WSW naar leeftijd 35-44': list_verzuim_wsw_naar_leeftijd_35_44,
            'Verzuim WSW naar leeftijd 45-54':list_verzuim_wsw_naar_leeftijd_45_54,
            'Verzuim WSW naar leeftijd 55':list_verzuim_wsw_naar_leeftijd_55,
            'Verzuim PW naar leeftijd 25': list_verzuim_PW_naar_leeftijd_25,
            'Verzuim PW naar leeftijd 25-34': list_verzuim_PW_naar_leeftijd_25_34,
            'Verzuim PW naar leeftijd 35-44': list_verzuim_PW_naar_leeftijd_35_44,
            'Verzuim PW naar leeftijd 45-54':list_verzuim_PW_naar_leeftijd_45_54,
            'Verzuim PW naar leeftijd 55':list_verzuim_PW_naar_leeftijd_55,
            'Verzuim Ander naar leeftijd 25': list_verzuim_ander_naar_leeftijd_25,
            'Verzuim Ander naar leeftijd 25-34': list_verzuim_ander_naar_leeftijd_25_34,
            'Verzuim Ander naar leeftijd 35-44': list_verzuim_ander_naar_leeftijd_35_44,
            'Verzuim Ander naar leeftijd 45-54': list_verzuim_ander_naar_leeftijd_45_54,
            'Verzuim Ander naar leeftijd 55': list_verzuim_ander_naar_leeftijd_55,
            'Verzuim percentage man WSW': list_verzuim_perc_man_wsw,
            'Verzuim percentage vrouw WSW': list_verzuim_perc_vrouw_wsw,
            'Verzuim percentage man PW': list_verzuim_perc_man_PW,
            'Verzuim percentage vrouw PW': list_verzuim_perc_vrouw_PW,
            'Verzuim percentage man Ander': list_verzuim_perc_man_ander,
            'Verzuim percentage vrouw Ander': list_verzuim_perc_vrouw_ander,
            'Gemiddelde meldingsfrequentie WSW': list_gemiddelde_meldingsfrequentie_wsw,
            'Gemiddelde meldingsfrequentie PW': list_gemiddelde_meldingsfrequentie_PW,
            'Gemiddelde meldingsfrequentie Ander': list_gemiddelde_meldingsfrequentie_ander,
            'Gemiddelde verzuimduur WSW': list_gemiddelde_verzuimduur_wsw,
            'Gemiddelde verzuimduur PW': list_gemiddelde_verzuimduur_PW,
            'Gemiddelde verzuimduur Ander': list_gemiddelde_verzuimduur_ander,
            'Controle WSW verzuim naar leeftijd': list_controle_wsw_verzuim_naar_leeftijd,
            'Controle PW verzuim naar leeftijd': list_controle_PW_verzuim_naar_leeftijd,
            'Controle Ander verzuim naar leeftijd': list_controle_ander_verzuim_naar_leeftijd,
            'Controle WSW verzuim naar geslacht': list_controle_wsw_verzuim_naar_geslacht,
            'Controle PW verzuim naar geslacht': list_controle_PW_verzuim_naar_geslacht,
            'Controle Ander verzuim naar geslacht': list_controle_ander_verzuim_naar_geslacht
        }
        
        gemiddelde_verzuimduur_wsw_dienstverband = sum(list_gemiddelde_verzuimduur_wsw)/sum(list_person_wsw)
        gemiddelde_verzuimduur_PW_dienstverband = sum(list_gemiddelde_verzuimduur_PW)/sum(list_person_PW)
        gemiddelde_verzuimduur_ander_dienstverband = sum(list_gemiddelde_verzuimduur_ander)/sum(list_person_ander)

        totaal_personeel_naar_geslacht_wsw_dienstverband = sum(list_man_wsw) + sum(list_vrouw_wsw)
        totaal_personeel_naar_geslacht_Ander_dienstverband = sum(list_man_ander) + sum(list_vrouw_ander)
        totaal_personeel_naar_geslacht_PW_dienstverband = sum(list_man_PW) + sum(list_vrouw_PW)
        totaal_personeel_naar_geslacht_totaal = (sum(list_man_wsw) + sum(list_man_ander)) + + sum(list_man_PW)+ sum(list_vrouw_PW)+ (sum(list_vrouw_wsw) + sum(list_vrouw_ander))

        bm_gemiddelde_verzuimduur_totaal = (gemiddelde_verzuimduur_wsw_dienstverband*totaal_personeel_naar_geslacht_wsw_dienstverband
                                            + gemiddelde_verzuimduur_PW_dienstverband*totaal_personeel_naar_geslacht_PW_dienstverband
                                            + gemiddelde_verzuimduur_ander_dienstverband*totaal_personeel_naar_geslacht_Ander_dienstverband)/totaal_personeel_naar_geslacht_totaal
        
    ########### GRAFIEK 3: VERZUIMPERCENTAGE NAAR GESLACHT #############
    for bedrijf in df_data.index:

        ### Define Series
        srs_bdrf = df_data.iloc[bedrijf]

        wsw_dienstverband_man = srs_bdrf['manWSW']
        wsw_dienstverband_vrouw = srs_bdrf['vrouwWSW']
        PW_dienstverband_man = srs_bdrf['manPW']
        PW_dienstverband_vrouw = srs_bdrf['vrouwPW']
        ander_dienstverband_man = srs_bdrf['manAnder']
        ander_dienstverband_vrouw = srs_bdrf['vrouwAnder']
        personeel_naar_geslacht_totaal_man = wsw_dienstverband_man + ander_dienstverband_man + PW_dienstverband_man
        personeel_naar_geslacht_totaal_vrouw = wsw_dienstverband_vrouw + ander_dienstverband_vrouw + PW_dienstverband_vrouw
        totaal_personeel_wsw_dienstverband = wsw_dienstverband_man + wsw_dienstverband_vrouw
        totaal_personeel_PW_dienstverband = PW_dienstverband_man + PW_dienstverband_vrouw
        totaal_personeel_ander_dienstverband = ander_dienstverband_man + ander_dienstverband_vrouw
        totaal_personeel_naar_geslacht = personeel_naar_geslacht_totaal_man + personeel_naar_geslacht_totaal_vrouw
        calc_verzuimpercentage_naar_geslacht_totaal_man = (srs_bdrf["Verz_man_WSW"] * totaal_personeel_wsw_dienstverband +srs_bdrf["Verz_man_PW"] * totaal_personeel_PW_dienstverband + srs_bdrf["Verz_man_Ander"]*totaal_personeel_ander_dienstverband)/totaal_personeel_naar_geslacht
        calc_verzuimpercentage_naar_geslacht_totaal_vrouw = (srs_bdrf["Verz_vrouw_WSW"] * totaal_personeel_wsw_dienstverband +srs_bdrf["Verz_vrouw_PW"] * totaal_personeel_PW_dienstverband + + srs_bdrf["Verz_vrouw_Ander"]*totaal_personeel_ander_dienstverband)/totaal_personeel_naar_geslacht
        
        ### verzuimpercentage 
        calc_bm_verzuimpercentage_naar_geslacht_wsw_man = sum(list_verzuim_perc_man_wsw)/sum(list_man_wsw)
        calc_bm_verzuimpercentage_naar_geslacht_ander_man = sum(list_verzuim_perc_man_ander)/sum(list_man_ander)
        calc_bm_verzuimpercentage_naar_geslacht_PW_man = sum(list_verzuim_perc_man_PW)/sum(list_man_PW)
        calc_bm_verzuimpercentage_naar_geslacht_man_totaal = (calc_bm_verzuimpercentage_naar_geslacht_wsw_man * totaal_personeel_naar_geslacht_wsw_dienstverband + calc_bm_verzuimpercentage_naar_geslacht_PW_man*totaal_personeel_naar_geslacht_PW_dienstverband + calc_bm_verzuimpercentage_naar_geslacht_ander_man * totaal_personeel_naar_geslacht_Ander_dienstverband)/totaal_personeel_naar_geslacht_totaal

        calc_bm_verzuimpercentage_naar_geslacht_wsw_vrouw = sum(list_verzuim_perc_vrouw_wsw)/sum(list_vrouw_wsw)
        calc_bm_verzuimpercentage_naar_geslacht_ander_vrouw = sum(list_verzuim_perc_vrouw_ander)/sum(list_vrouw_ander)
        calc_bm_verzuimpercentage_naar_geslacht_PW_vrouw = sum(list_verzuim_perc_vrouw_PW)/sum(list_vrouw_PW)
        calc_bm_verzuimpercentage_naar_geslacht_vrouw_totaal = (calc_bm_verzuimpercentage_naar_geslacht_wsw_vrouw * totaal_personeel_naar_geslacht_wsw_dienstverband +calc_bm_verzuimpercentage_naar_geslacht_PW_vrouw*totaal_personeel_naar_geslacht_PW_dienstverband + calc_bm_verzuimpercentage_naar_geslacht_ander_vrouw * totaal_personeel_naar_geslacht_Ander_dienstverband)/totaal_personeel_naar_geslacht_totaal
        
        data = {'Type Dienstverband' : ["Wsw","PW","Overige", "Totaal", "Benchmark", "Wsw", "PW","Overige", "Totaal", "Benchmark"], 
            'Geslacht' : ["Man", "Man","Man", "Man", "Man", "Vrouw","Vrouw", "Vrouw", "Vrouw", "Vrouw"], 
            'Verzuimpercentage' :
            [srs_bdrf["Verz_man_WSW"]/100,srs_bdrf["Verz_man_PW"]/100, srs_bdrf["Verz_man_Ander"]/100, calc_verzuimpercentage_naar_geslacht_totaal_man/100, (calc_bm_verzuimpercentage_naar_geslacht_man_totaal), 
            srs_bdrf["Verz_vrouw_WSW"]/100,srs_bdrf["Verz_vrouw_PW"]/100,srs_bdrf["Verz_vrouw_Ander"]/100, calc_verzuimpercentage_naar_geslacht_totaal_vrouw/100, (calc_bm_verzuimpercentage_naar_geslacht_vrouw_totaal)]}
        
        print(data)
        
    return data


#adding a route to the flask server with the url /sum
@app.route("/verzuimduur", methods=['GET'])
def verzuimduur():
    
    response = requests.get('http://127.0.0.1:5006/query-data')
    if response.status_code == 200:
        data = response.json()
        
        df_data= pd.DataFrame.from_dict(data['df_data'])
        df_quartiles_verzuimpercentage = pd.DataFrame.from_dict(data['df_quartiles_verzuimpercentage'])
        df_quartiles_verzuimfrequentie = pd.DataFrame.from_dict(data['df_quartiles_verzuimfrequentie'])
        
        # Benchmark Dataframe
        list_verzuim_wsw = []
        list_verzuim_ander = []
        list_verzuim_PW = []
        list_verzuim_wsw_naar_leeftijd_25 = []
        list_verzuim_wsw_naar_leeftijd_25_34 = []
        list_verzuim_wsw_naar_leeftijd_35_44 = []
        list_verzuim_wsw_naar_leeftijd_45_54 = []
        list_verzuim_wsw_naar_leeftijd_55 = []
        list_verzuim_ander_naar_leeftijd_25 = []
        list_verzuim_ander_naar_leeftijd_25_34 = []
        list_verzuim_ander_naar_leeftijd_35_44 = []
        list_verzuim_ander_naar_leeftijd_45_54 = []
        list_verzuim_ander_naar_leeftijd_55 = []
        list_verzuim_PW_naar_leeftijd_25 = []
        list_verzuim_PW_naar_leeftijd_25_34 = []
        list_verzuim_PW_naar_leeftijd_35_44 = []
        list_verzuim_PW_naar_leeftijd_45_54 = []
        list_verzuim_PW_naar_leeftijd_55 = []
        list_verzuim_perc_man_wsw = []
        list_verzuim_perc_vrouw_wsw = []
        list_verzuim_perc_man_ander = []
        list_verzuim_perc_vrouw_ander = []
        list_verzuim_perc_man_PW = []
        list_verzuim_perc_vrouw_PW = []
        list_gemiddelde_meldingsfrequentie_wsw = []
        list_gemiddelde_meldingsfrequentie_ander = []
        list_gemiddelde_meldingsfrequentie_PW = []
        list_gemiddelde_verzuimduur_wsw =[]
        list_gemiddelde_verzuimduur_PW =[]
        list_gemiddelde_verzuimduur_ander = []
        list_controle_wsw_verzuim_naar_leeftijd = []
        list_controle_PW_verzuim_naar_leeftijd = []
        list_controle_ander_verzuim_naar_leeftijd = []
        list_controle_wsw_verzuim_naar_geslacht = []
        list_controle_PW_verzuim_naar_geslacht = []
        list_controle_ander_verzuim_naar_geslacht = []
        list_person_wsw = []
        list_person_ander = []
        list_person_PW = []
        list_man_wsw = []
        list_man_PW = []
        list_vrouw_wsw = []
        list_man_ander = []
        list_vrouw_ander = []
        list_vrouw_PW = []

        for bedrijf in df_data.index:
            ### Verzuim WSW # Column 1
            srs_bdrf = df_data.iloc[bedrijf]

            list_person_wsw.append(srs_bdrf['Person_WSW'])
            list_person_ander.append(srs_bdrf['Person_ander'])
            list_person_PW.append(srs_bdrf['Person_PW'])

            list_man_wsw.append(srs_bdrf['manWSW'])
            list_vrouw_wsw.append(srs_bdrf['vrouwWSW'])
            list_man_ander.append(srs_bdrf['manAnder'])
            list_vrouw_ander.append(srs_bdrf['vrouwAnder'])

            list_man_PW.append(srs_bdrf['manPW'])
            list_vrouw_PW.append(srs_bdrf['vrouwPW'])
            
            calc_verzuim_wsw = (srs_bdrf['tot_verz_WSW']/100)*srs_bdrf['Person_WSW']
            list_verzuim_wsw.append(calc_verzuim_wsw)

            ### Verzuim Ander # Column 2
            calc_verzuim_ander = srs_bdrf['Person_ander']*(srs_bdrf['tot_verz_Ander']/100)
            list_verzuim_ander.append(calc_verzuim_ander)

            ### Verzuim PW
            calc_verzuim_PW = srs_bdrf['Person_PW']*(srs_bdrf['tot_verz_PW']/100)
            list_verzuim_PW.append(calc_verzuim_PW)

            ### Verzuim WSW naar leeftijd 25
            calc_verzuim_wsw_naar_leeftijd_25 = (srs_bdrf['Verz_WSW25']/100)*srs_bdrf['WSW25']
            list_verzuim_wsw_naar_leeftijd_25.append(calc_verzuim_wsw_naar_leeftijd_25)

            ### Verzuim WSW naar leeftijd 25-34
            calc_verzuim_wsw_naar_leeftijd_25_34 = (srs_bdrf['Verz_WSW25_34']/100)*srs_bdrf['WSW25_34']
            list_verzuim_wsw_naar_leeftijd_25_34.append(calc_verzuim_wsw_naar_leeftijd_25_34)

            ### Verzuim WSW naar leeftijd 35-44
            calc_verzuim_wsw_naar_leeftijd_35_44 = (srs_bdrf['Verz_WSW35_44']/100)*srs_bdrf['WSW35_44']
            list_verzuim_wsw_naar_leeftijd_35_44.append(calc_verzuim_wsw_naar_leeftijd_35_44)

            ### Verzuim WSW naar leeftijd 45-54
            calc_verzuim_wsw_naar_leeftijd_45_54 = (srs_bdrf['Verz_WSW45_54']/100)*srs_bdrf['WSW45_54']
            list_verzuim_wsw_naar_leeftijd_45_54.append(calc_verzuim_wsw_naar_leeftijd_45_54)

            ### Verzuim WSW naar leeftijd 55
            calc_verzuim_wsw_naar_leeftijd_55 = (srs_bdrf['Verz_WSW55']/100)*srs_bdrf['WSW55']
            list_verzuim_wsw_naar_leeftijd_55.append(calc_verzuim_wsw_naar_leeftijd_55)

            ### Verzuim PW naar leeftijd 25
            calc_verzuim_PW_naar_leeftijd_25 = (srs_bdrf['Verz_PW25']/100)*srs_bdrf['PW25']
            list_verzuim_PW_naar_leeftijd_25.append(calc_verzuim_PW_naar_leeftijd_25)

            ### Verzuim PW naar leeftijd 25-34
            calc_verzuim_PW_naar_leeftijd_25_34 = (srs_bdrf['Verz_PW25_34']/100)*srs_bdrf['PW25_34']
            list_verzuim_PW_naar_leeftijd_25_34.append(calc_verzuim_PW_naar_leeftijd_25_34)

            ### Verzuim PW naar leeftijd 35-44
            calc_verzuim_PW_naar_leeftijd_35_44 = (srs_bdrf['Verz_PW35_44']/100)*srs_bdrf['PW35_44']
            list_verzuim_PW_naar_leeftijd_35_44.append(calc_verzuim_PW_naar_leeftijd_35_44)

            ### Verzuim PW naar leeftijd 45-54
            calc_verzuim_PW_naar_leeftijd_45_54 = (srs_bdrf['Verz_PW45_54']/100)*srs_bdrf['PW45_54']
            list_verzuim_PW_naar_leeftijd_45_54.append(calc_verzuim_PW_naar_leeftijd_45_54)

            ### Verzuim PW naar leeftijd 55
            calc_verzuim_PW_naar_leeftijd_55 = (srs_bdrf['Verz_PW55']/100)*srs_bdrf['PW55']
            list_verzuim_PW_naar_leeftijd_55.append(calc_verzuim_PW_naar_leeftijd_55)

            ### Verzuim Ander naar leeftijd 25
            calc_verzuim_ander_naar_leeftijd_25 = (srs_bdrf['Verz_Ander25']/100)*srs_bdrf['Ander25']
            list_verzuim_ander_naar_leeftijd_25.append(calc_verzuim_ander_naar_leeftijd_25)

            ### Verzuim Ander naar leeftijd 25-34
            calc_verzuim_ander_naar_leeftijd_25_34 = (srs_bdrf['Verz_Ander25_34']/100)*srs_bdrf['Ander25_34']
            list_verzuim_ander_naar_leeftijd_25_34.append(calc_verzuim_ander_naar_leeftijd_25_34)

            ### Verzuim Ander naar leeftijd 35-44
            calc_verzuim_ander_naar_leeftijd_35_44 = (srs_bdrf['Verz_Ander35_44']/100)*srs_bdrf['Ander35_44']
            list_verzuim_ander_naar_leeftijd_35_44.append(calc_verzuim_ander_naar_leeftijd_35_44)

            ### Verzuim Ander naar leeftijd 45-54
            calc_verzuim_ander_naar_leeftijd_45_54 = (srs_bdrf['Verz_Ander45_54']/100)*srs_bdrf['Ander45_54']
            list_verzuim_ander_naar_leeftijd_45_54.append(calc_verzuim_ander_naar_leeftijd_45_54)

            ### Verzuim Ander naar leeftijd 45-54
            calc_verzuim_ander_naar_leeftijd_55 = (srs_bdrf['Verz_Ander55']/100)*srs_bdrf['Ander55']
            list_verzuim_ander_naar_leeftijd_55.append(calc_verzuim_ander_naar_leeftijd_55)

            ### Verzuim percentage man WSW
            calc_verzuim_perc_man_wsw = (srs_bdrf['Verz_man_WSW']/100)*srs_bdrf['manWSW']
            list_verzuim_perc_man_wsw.append(calc_verzuim_perc_man_wsw)

            ### Verzuim percentage vrouw WSW
            calc_verzuim_perc_vrouw_wsw = (srs_bdrf['Verz_vrouw_WSW']/100)*srs_bdrf['vrouwWSW']
            list_verzuim_perc_vrouw_wsw.append(calc_verzuim_perc_vrouw_wsw)

            ### Verzuim percentage man Ander
            calc_verzuim_perc_man_ander = (srs_bdrf['Verz_man_Ander']/100)*srs_bdrf['manAnder']
            list_verzuim_perc_man_ander.append(calc_verzuim_perc_man_ander)

            ### Verzuim percentage vrouw Ander
            calc_verzuim_perc_vrouw_ander = (srs_bdrf['Verz_vrouw_Ander']/100)*srs_bdrf['vrouwAnder']
            list_verzuim_perc_vrouw_ander.append(calc_verzuim_perc_vrouw_ander)

            ### Verzuim percentage man PW
            calc_verzuim_perc_man_PW = (srs_bdrf['Verz_man_PW']/100)*srs_bdrf['manPW']
            list_verzuim_perc_man_PW.append(calc_verzuim_perc_man_PW)

            ### Verzuim percentage vrouw PW
            calc_verzuim_perc_vrouw_PW = (srs_bdrf['Verz_vrouw_PW']/100)*srs_bdrf['vrouwPW']
            list_verzuim_perc_vrouw_PW.append(calc_verzuim_perc_vrouw_PW)

            ### Gemiddelde meldingsfrequentie WSW
            calc_gemiddelde_meldingsfrequentie_wsw = srs_bdrf['Tot_gem_meldfreq_WSW1']*srs_bdrf['Person_WSW']
            list_gemiddelde_meldingsfrequentie_wsw.append(calc_gemiddelde_meldingsfrequentie_wsw)

            ### Gemiddelde meldingsfrequentie Ander
            calc_gemiddelde_meldingsfrequentie_ander = srs_bdrf['Tot_gem_meldfreq_Ander']*srs_bdrf['Person_ander']
            list_gemiddelde_meldingsfrequentie_ander.append(calc_gemiddelde_meldingsfrequentie_ander)

            ### Gemiddelde meldingsfrequentie PW
            calc_gemiddelde_meldingsfrequentie_PW = srs_bdrf['Tot_gem_meldfreq_PW']*srs_bdrf['Person_PW']
            list_gemiddelde_meldingsfrequentie_PW.append(calc_gemiddelde_meldingsfrequentie_PW)

            ### Gemiddelde verzuimduur WSW
            calc_gemiddelde_verzuimduur_wsw = srs_bdrf['Gem_verzd_WSW']*srs_bdrf['Person_WSW']
            list_gemiddelde_verzuimduur_wsw.append(calc_gemiddelde_verzuimduur_wsw)

            ### Gemiddelde verzuimduur PW
            calc_gemiddelde_verzuimduur_PW = srs_bdrf['Gem_verzd_PW']*srs_bdrf['Person_PW']
            list_gemiddelde_verzuimduur_PW.append(calc_gemiddelde_verzuimduur_PW)
            
            ### Gemiddelde verzuimduur Ander
            calc_gemiddelde_verzuimduur_ander = srs_bdrf['Gem_verzd_Ander']*srs_bdrf['Person_ander']
            list_gemiddelde_verzuimduur_ander.append(calc_gemiddelde_verzuimduur_ander)

            ### Controle WSW verzuim naar leeftijd
            calc_controle_wsw_verzuim_naar_leeftijd = calc_verzuim_wsw - (calc_verzuim_wsw_naar_leeftijd_25 + calc_verzuim_wsw_naar_leeftijd_25_34 
                + calc_verzuim_wsw_naar_leeftijd_35_44 + calc_verzuim_wsw_naar_leeftijd_45_54 + calc_verzuim_wsw_naar_leeftijd_55)
            list_controle_wsw_verzuim_naar_leeftijd.append(calc_controle_wsw_verzuim_naar_leeftijd)

            ### Controle PW verzuim naar leeftijd
            calc_controle_PW_verzuim_naar_leeftijd = calc_verzuim_PW - (calc_verzuim_PW_naar_leeftijd_25 + calc_verzuim_PW_naar_leeftijd_25_34 
                + calc_verzuim_PW_naar_leeftijd_35_44 + calc_verzuim_PW_naar_leeftijd_45_54 + calc_verzuim_PW_naar_leeftijd_55)
            list_controle_PW_verzuim_naar_leeftijd.append(calc_controle_PW_verzuim_naar_leeftijd)

            ### Controle Ander verzuim naar leeftijd
            calc_controle_ander_verzuim_naar_leeftijd = calc_verzuim_ander - (calc_verzuim_ander_naar_leeftijd_25 + calc_verzuim_ander_naar_leeftijd_25_34 
                + calc_verzuim_ander_naar_leeftijd_35_44 + calc_verzuim_ander_naar_leeftijd_45_54 + calc_verzuim_ander_naar_leeftijd_55)
            list_controle_ander_verzuim_naar_leeftijd.append(calc_controle_ander_verzuim_naar_leeftijd)

            ### Controle WSW verzuim naar geslacht
            calc_controle_wsw_verzuim_naar_geslacht = calc_verzuim_wsw - calc_verzuim_perc_man_wsw - calc_verzuim_perc_vrouw_wsw
            list_controle_wsw_verzuim_naar_geslacht.append(calc_controle_wsw_verzuim_naar_geslacht)

            ### Controle PW verzuim naar geslacht
            calc_controle_PW_verzuim_naar_geslacht = calc_verzuim_PW - calc_verzuim_perc_man_PW - calc_verzuim_perc_vrouw_PW
            list_controle_PW_verzuim_naar_geslacht.append(calc_controle_PW_verzuim_naar_geslacht)

            ### Controle Ander verzuim naar geslacht
            calc_controle_ander_verzuim_naar_geslacht = calc_verzuim_ander - calc_verzuim_perc_man_ander - calc_verzuim_perc_vrouw_ander
            list_controle_ander_verzuim_naar_geslacht.append(calc_controle_ander_verzuim_naar_geslacht)

            #Replace nan with ""
            list_verzuim_wsw = [0 if math.isnan(x) else x for x in list_verzuim_wsw]
            list_verzuim_PW = [0 if math.isnan(x) else x for x in list_verzuim_PW]
            list_verzuim_ander = [0 if math.isnan(x) else x for x in list_verzuim_ander]
            list_verzuim_wsw_naar_leeftijd_25 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_25]
            list_verzuim_wsw_naar_leeftijd_25_34 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_25_34]
            list_verzuim_wsw_naar_leeftijd_35_44 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_35_44]
            list_verzuim_wsw_naar_leeftijd_45_54 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_45_54]
            list_verzuim_wsw_naar_leeftijd_55 = [0 if math.isnan(x) else x for x in list_verzuim_wsw_naar_leeftijd_55]
            list_verzuim_PW_naar_leeftijd_25 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_25]
            list_verzuim_PW_naar_leeftijd_25_34 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_25_34]
            list_verzuim_PW_naar_leeftijd_35_44 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_35_44]
            list_verzuim_PW_naar_leeftijd_45_54 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_45_54]
            list_verzuim_PW_naar_leeftijd_55 = [0 if math.isnan(x) else x for x in list_verzuim_PW_naar_leeftijd_55]
            list_verzuim_ander_naar_leeftijd_25 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_25]
            list_verzuim_ander_naar_leeftijd_25_34 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_25_34]
            list_verzuim_ander_naar_leeftijd_35_44 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_35_44]
            list_verzuim_ander_naar_leeftijd_45_54 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_45_54]
            list_verzuim_ander_naar_leeftijd_55 = [0 if math.isnan(x) else x for x in list_verzuim_ander_naar_leeftijd_55]
            list_verzuim_perc_man_wsw = [0 if math.isnan(x) else x for x in list_verzuim_perc_man_wsw]
            list_verzuim_perc_vrouw_wsw = [0 if math.isnan(x) else x for x in list_verzuim_perc_vrouw_wsw]
            list_verzuim_perc_man_PW = [0 if math.isnan(x) else x for x in list_verzuim_perc_man_PW]
            list_verzuim_perc_vrouw_PW = [0 if math.isnan(x) else x for x in list_verzuim_perc_vrouw_PW]
            list_verzuim_perc_man_ander = [0 if math.isnan(x) else x for x in list_verzuim_perc_man_ander]
            list_verzuim_perc_vrouw_ander = [0 if math.isnan(x) else x for x in list_verzuim_perc_vrouw_ander]
            list_gemiddelde_meldingsfrequentie_wsw = [0 if math.isnan(x) else x for x in list_gemiddelde_meldingsfrequentie_wsw]
            list_gemiddelde_meldingsfrequentie_PW = [0 if math.isnan(x) else x for x in list_gemiddelde_meldingsfrequentie_PW]
            list_gemiddelde_meldingsfrequentie_ander = [0 if math.isnan(x) else x for x in list_gemiddelde_meldingsfrequentie_ander]
            list_gemiddelde_verzuimduur_wsw = [0 if math.isnan(x) else x for x in list_gemiddelde_verzuimduur_wsw]
            list_gemiddelde_verzuimduur_PW = [0 if math.isnan(x) else x for x in list_gemiddelde_verzuimduur_PW]
            list_gemiddelde_verzuimduur_ander = [0 if math.isnan(x) else x for x in list_gemiddelde_verzuimduur_ander]
            list_controle_wsw_verzuim_naar_leeftijd = [0 if math.isnan(x) else x for x in list_controle_wsw_verzuim_naar_leeftijd]
            list_controle_PW_verzuim_naar_leeftijd = [0 if math.isnan(x) else x for x in list_controle_PW_verzuim_naar_leeftijd]
            list_controle_ander_verzuim_naar_leeftijd = [0 if math.isnan(x) else x for x in list_controle_ander_verzuim_naar_leeftijd]
            list_controle_wsw_verzuim_naar_geslacht = [0 if math.isnan(x) else x for x in list_controle_wsw_verzuim_naar_geslacht]
            list_controle_PW_verzuim_naar_geslacht = [0 if math.isnan(x) else x for x in list_controle_PW_verzuim_naar_geslacht]
            list_controle_ander_verzuim_naar_geslacht = [0 if math.isnan(x) else x for x in list_controle_ander_verzuim_naar_geslacht]
            list_person_wsw = [0 if math.isnan(x) else x for x in list_person_wsw]
            list_person_PW = [0 if math.isnan(x) else x for x in list_person_PW]
            list_person_ander = [0 if math.isnan(x) else x for x in list_person_ander]
            list_man_wsw = [0 if math.isnan(x) else x for x in list_man_wsw]
            list_vrouw_wsw = [0 if math.isnan(x) else x for x in list_vrouw_wsw]
            list_man_PW = [0 if math.isnan(x) else x for x in list_man_PW]
            list_vrouw_PW = [0 if math.isnan(x) else x for x in list_vrouw_PW]
            list_man_ander = [0 if math.isnan(x) else x for x in list_man_ander]
            list_vrouw_ander = [0 if math.isnan(x) else x for x in list_vrouw_ander]

            benchmark_data = {
                'Verzuim WSW': list_verzuim_wsw,
                'Verzuim PW': list_verzuim_PW,
                'Verzuim Ander': list_verzuim_ander,
                'Verzuim WSW naar leeftijd 25': list_verzuim_wsw_naar_leeftijd_25,
                'Verzuim WSW naar leeftijd 25-34': list_verzuim_wsw_naar_leeftijd_25_34,
                'Verzuim WSW naar leeftijd 35-44': list_verzuim_wsw_naar_leeftijd_35_44,
                'Verzuim WSW naar leeftijd 45-54':list_verzuim_wsw_naar_leeftijd_45_54,
                'Verzuim WSW naar leeftijd 55':list_verzuim_wsw_naar_leeftijd_55,
                'Verzuim PW naar leeftijd 25': list_verzuim_PW_naar_leeftijd_25,
                'Verzuim PW naar leeftijd 25-34': list_verzuim_PW_naar_leeftijd_25_34,
                'Verzuim PW naar leeftijd 35-44': list_verzuim_PW_naar_leeftijd_35_44,
                'Verzuim PW naar leeftijd 45-54':list_verzuim_PW_naar_leeftijd_45_54,
                'Verzuim PW naar leeftijd 55':list_verzuim_PW_naar_leeftijd_55,
                'Verzuim Ander naar leeftijd 25': list_verzuim_ander_naar_leeftijd_25,
                'Verzuim Ander naar leeftijd 25-34': list_verzuim_ander_naar_leeftijd_25_34,
                'Verzuim Ander naar leeftijd 35-44': list_verzuim_ander_naar_leeftijd_35_44,
                'Verzuim Ander naar leeftijd 45-54': list_verzuim_ander_naar_leeftijd_45_54,
                'Verzuim Ander naar leeftijd 55': list_verzuim_ander_naar_leeftijd_55,
                'Verzuim percentage man WSW': list_verzuim_perc_man_wsw,
                'Verzuim percentage vrouw WSW': list_verzuim_perc_vrouw_wsw,
                'Verzuim percentage man PW': list_verzuim_perc_man_PW,
                'Verzuim percentage vrouw PW': list_verzuim_perc_vrouw_PW,
                'Verzuim percentage man Ander': list_verzuim_perc_man_ander,
                'Verzuim percentage vrouw Ander': list_verzuim_perc_vrouw_ander,
                'Gemiddelde meldingsfrequentie WSW': list_gemiddelde_meldingsfrequentie_wsw,
                'Gemiddelde meldingsfrequentie PW': list_gemiddelde_meldingsfrequentie_PW,
                'Gemiddelde meldingsfrequentie Ander': list_gemiddelde_meldingsfrequentie_ander,
                'Gemiddelde verzuimduur WSW': list_gemiddelde_verzuimduur_wsw,
                'Gemiddelde verzuimduur PW': list_gemiddelde_verzuimduur_PW,
                'Gemiddelde verzuimduur Ander': list_gemiddelde_verzuimduur_ander,
                'Controle WSW verzuim naar leeftijd': list_controle_wsw_verzuim_naar_leeftijd,
                'Controle PW verzuim naar leeftijd': list_controle_PW_verzuim_naar_leeftijd,
                'Controle Ander verzuim naar leeftijd': list_controle_ander_verzuim_naar_leeftijd,
                'Controle WSW verzuim naar geslacht': list_controle_wsw_verzuim_naar_geslacht,
                'Controle PW verzuim naar geslacht': list_controle_PW_verzuim_naar_geslacht,
                'Controle Ander verzuim naar geslacht': list_controle_ander_verzuim_naar_geslacht
            }

        df_benchmark = pd.DataFrame(data=benchmark_data)
        
        gemiddelde_verzuimduur_wsw_dienstverband = sum(list_gemiddelde_verzuimduur_wsw)/sum(list_person_wsw)
        gemiddelde_verzuimduur_PW_dienstverband = sum(list_gemiddelde_verzuimduur_PW)/sum(list_person_PW)
        gemiddelde_verzuimduur_ander_dienstverband = sum(list_gemiddelde_verzuimduur_ander)/sum(list_person_ander)

        totaal_personeel_naar_geslacht_wsw_dienstverband = sum(list_man_wsw) + sum(list_vrouw_wsw)
        totaal_personeel_naar_geslacht_Ander_dienstverband = sum(list_man_ander) + sum(list_vrouw_ander)
        totaal_personeel_naar_geslacht_PW_dienstverband = sum(list_man_PW) + sum(list_vrouw_PW)
        totaal_personeel_naar_geslacht_totaal = (sum(list_man_wsw) + sum(list_man_ander)) + + sum(list_man_PW)+ sum(list_vrouw_PW)+ (sum(list_vrouw_wsw) + sum(list_vrouw_ander))

        bm_gemiddelde_verzuimduur_totaal = (gemiddelde_verzuimduur_wsw_dienstverband*totaal_personeel_naar_geslacht_wsw_dienstverband
                                            + gemiddelde_verzuimduur_PW_dienstverband*totaal_personeel_naar_geslacht_PW_dienstverband
                                            + gemiddelde_verzuimduur_ander_dienstverband*totaal_personeel_naar_geslacht_Ander_dienstverband)/totaal_personeel_naar_geslacht_totaal
        for bedrijf in df_data.index:
            ### Define Series
            srs_bdrf = df_data.iloc[bedrijf]

            wsw_dienstverband_man = srs_bdrf['manWSW']
            wsw_dienstverband_vrouw = srs_bdrf['vrouwWSW']
            PW_dienstverband_man = srs_bdrf['manPW']
            PW_dienstverband_vrouw = srs_bdrf['vrouwPW']
            ander_dienstverband_man = srs_bdrf['manAnder']
            ander_dienstverband_vrouw = srs_bdrf['vrouwAnder']
            personeel_naar_geslacht_totaal_man = wsw_dienstverband_man + ander_dienstverband_man + PW_dienstverband_man
            personeel_naar_geslacht_totaal_vrouw = wsw_dienstverband_vrouw + ander_dienstverband_vrouw + PW_dienstverband_vrouw
            totaal_personeel_wsw_dienstverband = wsw_dienstverband_man + wsw_dienstverband_vrouw
            totaal_personeel_ander_dienstverband = ander_dienstverband_man + ander_dienstverband_vrouw
            totaal_personeel_PW_dienstverband = PW_dienstverband_man + PW_dienstverband_vrouw
            totaal_personeel_naar_geslacht = personeel_naar_geslacht_totaal_man + personeel_naar_geslacht_totaal_vrouw

            ### verzuimduur wsw-dienstverband
            calc_gemiddelde_verzuimduur_totaal = ((srs_bdrf["Gem_verzd_WSW"] * totaal_personeel_wsw_dienstverband + 
                                                srs_bdrf["Gem_verzd_PW"] * totaal_personeel_PW_dienstverband +
                                                srs_bdrf["Gem_verzd_Ander"]* totaal_personeel_ander_dienstverband)/totaal_personeel_naar_geslacht)
            
            data = {'Type Dienstverband' : ["Totaal", "Benchmark", "Grootteklasse", "1e Kwartiel"], 
            'Jaar' : ["2022", "2022", "2022", "2022"], 
            'Aantal Dagen' :
            [ calc_gemiddelde_verzuimduur_totaal, bm_gemiddelde_verzuimduur_totaal, def_grootteklasse_verzuimduur(calc_totaal_personen), def_kwartielen_verzuimduur(calc_totaal_personen) ]}
        
    
    return data
#running the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5015)