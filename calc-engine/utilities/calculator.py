import pandas as pd

class CalcData:
    def __init__(self, food_data):
        self.food_data = food_data

    def process_data(self):
        #Convert list of dictionaries to Pandas DataFrame
        df = pd.DataFrame(self.food_data, columns=['name', 'calories', 'protein', 'date'])
            
        df['date'] = pd.to_datetime(df['date'])
            
        df['week'] = df['date'].dt.isocalendar().week
            
        # Group the data by week and calculate the total calories and protein per week
        df_weekly = df.groupby('week').agg({'calories': 'sum', 'protein': 'sum'}).reset_index()

        #Convert DataFrame to JSON
        list_of_dicts = df_weekly.to_dict(orient='records')
            
        return list_of_dicts