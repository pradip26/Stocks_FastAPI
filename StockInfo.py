from MongoClient import Mongo

class StockInfo:

    mongoObj = ""
    stockInfoCollection = "stock_details"
    stockPriceCollection = 'stock_tradinginfo'

    def __init__(self):
        self.mongoObj = Mongo()

    def getStockDetails(self, symbol):
        condition = {
            'nsecode': symbol
        }
        data = self.mongoObj.getRecords(self.stockInfoCollection,condition)
        priceData = self.getPriceDetails(symbol)
        response = []
        for info in data:
            result = {
                "symbol" : info['nsecode'],
                'name': info['company_name'],
                'facevalue': info['face_value'],
                'industry': info['industry'],
                'short_name': info['short_name'],
                'status': info['status'],
                'price_info': priceData
            }
            response.append(result)
        return response

    def getPriceDetails(self, symbol):
        condition = {
            'symbol': symbol
        }
        response = []
        data = self.mongoObj.getRecords(self.stockPriceCollection, condition)
        for d in data:
            res = {
                'price': d['lastprice'],
                'change': d['change'],
                'change_p': d['change_perc'],
                'day_high': d['day_high'],
                'day_low': d['day_low'],
                'sector_pe': d['sector_pe'],
                'PE': d['PE'],
                'week_high': d['week_high'],
                'week_low': d['week_low'],
                'mcap': d['mcap'],
                'totalTradedValue': d['totalTradedValue']
            }
            response.append(res)
        return response
