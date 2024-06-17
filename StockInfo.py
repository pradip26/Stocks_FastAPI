from MongoClient import Mongo

class StockInfo:

    mongoObj = ""
    stockInfoCollection = "stock_details"
    stockPriceCollection = 'stock_tradinginfo'
    stockResultCollection = 'stock_results'
    stockCorpActionCollection = 'stock_corp_action'
    stockHistPriceCollection = 'stock_hist_prices'
    stockScoreCollection = 'stock_score'
    sampleModelPortfolioCollection = 'sample_model_portfolio'
    sampleModelPFDailyCollection = 'sample_model_pf_daily'

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
                'price_info': priceData[0]
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
                'totalTradedValue': d['totalTradedValue'],
                'last_traded_date': d['last_traded_date']
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

    def getHistPirces(self, symbol, fromDate="", toDate=""):

        if fromDate != "" and toDate != "":
            condition = {
                'symbol': symbol,
                'date':{"$gte": fromDate, "$lte":toDate}
            }
        elif fromDate != "" and toDate == "":
            condition = {
                'symbol': symbol,
                'date': {"$gte": fromDate}
            }
        elif fromDate == "" and toDate != "":
            condition = {
                'symbol': symbol,
                'date': {"$lte": toDate}
            }
        else:
            condition = {
                'symbol': symbol,
            }

        response = []
        fields = {"_id": 0, 'date': 1, 'close_price':1}
        sortFields = {"date": 1}

        data = self.mongoObj.getRecords(self.stockHistPriceCollection, condition, fields, sortFields)
        for d in data:
            res = dict(d)
            response.append(res)
        return response

    def getPeersList(self, industry):

        condition = {
            'sector': industry,
        }
        response = []
        fields = {"_id": 0,'symbol':1, 'lastprice':1, 'change_perc':1, 'PE':1, 'previousClose': 1}
        sortFields = {"PE": 1}
        data = self.mongoObj.getRecords(self.stockPriceCollection, condition, fields, sortFields)
        for d in data:
            res = dict(d)
            response.append(res)
        return response

    def getTopScoreStockList(self):
        condition = {"finance_grade":{"$in":["positive","very positive","flat"]},"valuation_grade":{"$in":["average","good"]}}
        response = []
        fields = {"_id": 0, 'symbol': 1, 'total_point': 1, 'date': 1, 'finance_grade': 1, 'valuation_grade': 1}
        sortFields = {"date":-1,"total_point": -1}
        data = self.mongoObj.getRecords(self.stockScoreCollection, condition, fields, sortFields,20)
        for d in data:
            res = dict(d)
            response.append(res)
        return response

    def getStockScore(self,symbol):
        condition = {"symbol":symbol}
        response = []
        fields = {"_id": 0, 'symbol': 1, 'total_point': 1, 'date': 1, 'finance_grade': 1, 'valuation_grade': 1, 'call':1}
        sortFields = {"date":-1,"total_point": -1}
        data = self.mongoObj.getRecords(self.stockScoreCollection, condition, fields, sortFields)
        for d in data:
            res = dict(d)
            response.append(res)
        return response

    def getSamplePF(self):
        condition = {}
        response = []
        fields = {"_id": 0}
        sortFields = {"date": -1}
        data = self.mongoObj.getRecords(self.sampleModelPortfolioCollection, condition, fields, sortFields)
        for d in data:
            res = dict(d)
            response.append(res)
        return response

    def getSampleLatestPortfolioData(self):
        condition = {}
        response = []
        fields = {"_id": 0}
        sortFields = {"date": -1}
        data = self.mongoObj.getRecords(self.sampleModelPFDailyCollection, condition, fields, sortFields,1)
        response = []
        for d in data:
            response = {
                "date" : d['date'],
                'type': d['type'],
                'current_pf_val': d['current_pf_val'],
                'gain': d['gain'],
                'gain_perc': d['gain_perc'],
                'invested_val': d['invested_val'],
            }
        return response

    def getSamplePortfolioWeeklyGraph(self):
        condition = {}
        response = []
        fields = {"_id": 0, "date": 1, "current_pf_val": 1, "gain": 1, "gain_perc": 1}
        sortFields = {"date": 1}
        data = self.mongoObj.getRecords(self.sampleModelPFDailyCollection, condition, fields, sortFields)
        for d in data:
            res = dict(d)
            response.append(res)
        return response
