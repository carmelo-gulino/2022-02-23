from database.DB_connect import DBConnect
from model.review import Review


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_cities():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct b.city from business b order by b.city """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row['city'])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_locali(city):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinctrow b.business_id , b.business_name 
        from business b 
        where b.city = %s
        order by b.business_name """
        cursor.execute(query, (city,))
        result = []
        for row in cursor:
            result.append((row['business_id'], row['business_name']))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_reviews(business_id):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from reviews r where r.business_id = %s"""
        cursor.execute(query, (business_id,))
        result = []
        for row in cursor:
            result.append(Review(**row))
        cursor.close()
        cnx.close()
        return result
