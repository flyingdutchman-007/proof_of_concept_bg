import json
from pathlib import Path
from typing import List
from flask import jsonify
import requests
import strawberry
import json

        
@strawberry.type
class FoodType:
    name: str
    calories: int
    protein: int
    date: str


@strawberry.type
class VerzuimVenster:
    Naam: List[str]
    Verzuimpercentage: List[float]
    GemiddeldeMeldingsfrequentie: List[float]
    label: List[str]
    verzuimfreqVenster: float
    verzuimpercVenster: float

@strawberry.type
class VerzuimPercentage:
    TypeDienstverband: List[str]
    Jaar: List[str]
    Verzuimpercentage: List[float]
    
@strawberry.type
class VerzuimPercentageGeslacht:
    Geslacht: List[str]
    TypeDienstverband: List[str]
    Verzuimpercentage: List[float]

@strawberry.input
class AddCalcFoodInput:
    week: int
    calories: int
    protein: int


@strawberry.type
class Query:

    @strawberry.field
    def food(self) -> List[FoodType]:
        response = requests.get('http://172.20.0.3:5006/query-food')
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: {response.status_code}")
        food_list = [
            FoodType(name=row[0], protein=row[1], calories=row[2], date=row[3])
            for row in data
        ]
        return food_list
   
    @strawberry.field
    def VerzuimPercentageGeslachtQuery(self) -> List[VerzuimPercentageGeslacht]:
        response = requests.get('http://127.0.0.1:5015/verzuimpercentagegeslacht')
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: {response.status_code}")
        
        VerzuimPercentageGeslachtData = [    VerzuimPercentageGeslacht(        
                Geslacht=row['Geslacht'],                                                       
                TypeDienstverband=row['Type Dienstverband'],
                Verzuimpercentage=row['Verzuimpercentage'],
            )
            for row in [data]
        ]
        return VerzuimPercentageGeslachtData    
    
    @strawberry.field
    def VerzuimPercentageQuery(self) -> List[VerzuimPercentage]:
        response = requests.get('http://calc-service:5015/verzuimpercentage')
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: {response.status_code}")
        
        VerzuimPercentageData = [    VerzuimPercentage(        TypeDienstverband=row['Type Dienstverband'],
                Jaar=row['Jaar'],
                Verzuimpercentage=row['Verzuimpercentage'],
            )
            for row in [data]
        ]
        return VerzuimPercentageData
    
    @strawberry.field
    def VerzuimVensterQuery(self) -> List[VerzuimVenster]:
        response = requests.get('http://calc-service:5015/verzuimvenster')
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: {response.status_code}")
        
        # data = {'Naam': ['WVS', '1e Kwartiel'], 'Verzuimpercentage': [16.20025445292621, 14.838207128456654], 'Gemiddelde meldingsfrequentie': [1.8223969465648853, 1.7360879993093987], 'label': ['WVS, 16.2%, 1.82', '1e Kwartiel, 14.8%, 1.74'], 'verzuimfreqVenster': 2.0106678147722925, 'verzuimpercVenster': 15.606863120295955}
        VerzuimVensterData = [    VerzuimVenster(        Naam=row['Naam'],
                Verzuimpercentage=row['Verzuimpercentage'],
                GemiddeldeMeldingsfrequentie=row['Gemiddelde meldingsfrequentie'],
                label=row['label'],
                verzuimfreqVenster=row['verzuimfreqVenster'],
                verzuimpercVenster=row['verzuimpercVenster']
            )
            for row in [data]
        ]
        
        return VerzuimVensterData

# @strawberry.type
# class Mutation:
#     def __init__(self):
#         self.test = []
        
#     @strawberry.mutation
#     def add_food(
#         self, name: str, calories: int, protein: int, date: str
#     ) -> FoodType:
#         print(name, calories, protein, date)
#         data = {
#             "name": name,
#             "calories": calories,
#             "protein": protein,
#             "date": date
#         }

#         try:
#             response = requests.post("http://0.0.0.0:5006/insert-food", json=data)
#             response.raise_for_status()
#             print("Data sent successfully")
#         except requests.exceptions.RequestException as error:
#             print("Error sending data:", error)

#         return FoodType(name=name, calories=calories, protein=protein, date=date)

    # @strawberry.mutation
    # def add_calc_food(self, input: List[AddCalcFoodInput]) -> str:
    #     json_data = json.dumps([vars(x) for x in input])
    #     print(json_data)

    #     try:
    #         response = requests.post("http://0.0.0.0:5085", json=json_data)
    #         response.raise_for_status()
    #         print("Data sent successfully")
    #     except requests.exceptions.RequestException as error:
    #         print("Error sending data:", error)
    #     # try:
    #     #     response = requests.post("http://0.0.0.0:5006/insert-calcfood", json=data)
    #     #     response.raise_for_status()
    #     #     print("Data sent successfully")
    #     # except requests.exceptions.RequestException as error:
    #     #     print("Error sending data:", error)
    
    #     return str(input)


schema = strawberry.Schema(query=Query)
