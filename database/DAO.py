from database.DB_connect import DBConnect
from model.arco import Arco
from model.order import Order


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getStore():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from stores s """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row["store_id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getOrders(storeId):  #sono i nodi
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from orders o 
                    where o.store_id = %s"""
        cursor.execute(query, (storeId, ))
        result = []
        for row in cursor:
            result.append(Order(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(storeId, kInt):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select t1.ordine1, t2.ordine2, t1.quantita1 + t2.quantita2 as peso
                    from (select o.order_id ordine1, o.store_id store1, o.order_date data1, sum(oi.quantity) as quantita1
                            from order_items oi, orders o 
                            where o.order_id = oi.order_id 
                            group by o.order_id) t1, 
                            (select o.order_id ordine2, o.store_id store2, o.order_date data2, sum(oi.quantity) as quantita2
                            from order_items oi, orders o 
                            where o.order_id = oi.order_id 
                            group by o.order_id) t2
                    where t1.ordine1 > t2.ordine2 and t1.store1 = t2.store2 and t1.store1= %s and datediff(t1.data1, t2.data2) < %s and datediff(t1.data1, t2.data2) > 0"""
        cursor.execute(query, (storeId, kInt))
        result = []
        for row in cursor:
            result.append(Arco(**row))
        cursor.close()
        conn.close()
        return result
