import psycopg2

class FoodData:
    def __init__(self,host,port,user,password,dbname):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )

    def insert_food(self,data):
        print(data['name'], data['calories'], data['protein'], data['date'])
        cursor = self.conn.cursor()
        cursor.execute(
        'INSERT INTO fooddata (name, calories, protein, date) VALUES (%s, %s, %s, %s)',
        (data['name'], data['calories'], data['protein'], data['date'])
        )
        self.conn.commit()
        cursor.close()

    def insert_calc_food(self,data): 
        cursor = self.conn.cursor()
        cursor.execute(
        'INSERT INTO foodcalcdata (name, calories, protein) VALUES (%s, %s, %s)',
        (data['name'], data['calories'], data['protein'])
        )
        self.conn.commit()
        cursor.close()

    def query_food(self):
        cursor = self.conn.cursor()
        cursor.execute(
          "SELECT * FROM fooddata")
        self.conn.commit()
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def query_calc_food(self):
        cursor = self.conn.cursor()
        cursor.execute(
          "SELECT name, protein, calories FROM foodcalcdata")
        self.conn.commit()
        rows = cursor.fetchall()
        cursor.close()
        return rows
