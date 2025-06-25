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
                    order by year(gds.`Date`)"""
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
            query = """select distinct *
                    from go_retailers gr
                     where gr.Country=%s"""
            cursor.execute(query,(nazione,))
            for row in cursor:
                res.append(Retailer(**row))

            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getArchiPesati(anno,nazione,idMap):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct gds.Retailer_code as r1, gds2.Retailer_code as r2, count(distinct gds2.Product_number) as peso 
                    from go_daily_sales gds, go_daily_sales gds2, go_retailers gr,go_retailers gr2 
                    where gds2.Product_number = gds.Product_number
                    and gr2.Retailer_code =gds2.Retailer_code 
                    and gr.Retailer_code =gds.Retailer_code
                    and gr2.Country =%s
                    and gr2.Country =gr.Country
                    and year(gds2.`Date`) =%s
                    and year(gds2.`Date`)= year(gds.`Date`)
                    and gds.Retailer_code>gds2.Retailer_code
                    group by r1,r2"""
            cursor.execute(query,(nazione,anno))
            for row in cursor:
                res.append((idMap[row["r1"]],idMap[row["r2"]],row["peso"]))

            cursor.close()
            cnx.close()
        return res



