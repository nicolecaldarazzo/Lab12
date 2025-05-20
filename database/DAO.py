from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getYears():
        cnx=DBConnect.get_connection()
        res=[]
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor=cnx.cursor(dictionary=True)
            query="""select distinct year(gds.`Date`) as anno
                    from go_daily_sales gds 
                    order by gds.`Date` """
            cursor.execute(query)
            for row in cursor:
                res.append(row["anno"])

            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getCountry():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct gr.Country as nazione
                        from go_retailers gr 
                        order by gr.Country """
            cursor.execute(query)
            for row in cursor:
                res.append(row["nazione"])

            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getNodiRetailers(nazione):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                    from go_retailers gr
                     where gr.Country=%s"""
            cursor.execute(query,(nazione,))
            for row in cursor:
                res.append(Retailer(**row))

            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getArchiPesati(anno,nazione):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                            from go_retailers gr """
            cursor.execute(query,(anno,nazione))
            for row in cursor:
                res.append(Retailer(**row))

            cursor.close()
            cnx.close()
        return res



