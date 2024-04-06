from MongoClient import Mongo

class StockInfo:

    mongoObj = ""
    stockInfoCollection = "stock_details"
    stockPriceCollection = 'stock_tradinginfo'
    stockResultCollection = 'stock_results'
    stockCorpActionCollection = 'stock_corp_action'

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

    def getResultDetails(self, symbol, resultType):
        condition = {
            'symbol': symbol,
        }

        if resultType == 'all':
            limit = sort = None
        else:
            limit = 1
            sort = {"to_date": -1}

        response = []
        fields = {"_id": 0, "symbol": 1 ,"income": 1, "eps": 1, "profit_after_tax": 1, "profit_before_tax": 1, "from_date": 1, "to_date": 1}
        data = self.mongoObj.getRecords(self.stockResultCollection, condition, fields, sort, limit)
        for d in data:
            res = dict(d)
            response.append(res)

        return response

    def getCorpActions(self, symbol):

        condition = {
            'symbol': symbol,
        }
        response = []
        fields = {"_id": 0}
        sortFields = {"exdate": -1}
        data = self.mongoObj.getRecords(self.stockCorpActionCollection, condition, fields, sortFields)
        for d in data:
            res = dict(d)
            response.append(res)
        return response