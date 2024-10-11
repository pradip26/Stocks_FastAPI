from MongoClient import Mongo


class IndexInfo:
    mongoObj = ""
    indexHistPriceCollection = "indices_hist_prices"
    indicesCollection = "indices"

    def __init__(self):
        self.mongoObj = Mongo()

    def getHistPirces(self, indexCode, fromDate="", toDate=""):

        if fromDate != "" and toDate != "":
            condition = {
                'indexcode': indexCode,
                'date': {"$gte": fromDate, "$lte": toDate}
            }
        elif fromDate != "" and toDate == "":
            condition = {
                'indexcode': indexCode,
                'date': {"$gte": fromDate}
            }
        elif fromDate == "" and toDate != "":
            condition = {
                'indexcode': indexCode,
                'date': {"$lte": toDate}
            }
        else:
            condition = {
                'indexcode': indexCode,
            }

        response = []
        fields = {"_id": 0, 'date': 1, 'close_price': 1, "open_price": 1, "day_high": 1, "day_low": 1}
        sortFields = {"date": 1}

        data = self.mongoObj.getRecords(self.indexHistPriceCollection, condition, fields, sortFields)
        for d in data:
            res = dict(d)
            response.append(res)
        return response

    def indexCalculations(self, data):
        count = 0
        list = []
        for priceData in data:
            price = priceData['close_price']
            date = priceData['date']
            dict = {}
            if count == 0:
                startIndex = 100
                dict = {
                    'price': price,
                    'date': date,
                    'index': startIndex
                }
                prevPrice = price
                prevIndex = startIndex
                count = count + 1
                list.append(dict)
            else:
                priceDiff = round(((price - prevPrice) / prevPrice) * 100, 2)
                indexVal = priceDiff + prevIndex
                prevPrice = price
                prevIndex = indexVal
                count = count + 1
                dict = {
                    'price': price,
                    'date': date,
                    'index': indexVal
                }
                list.append(dict)

        return list

    def getIndexDetails(self, indexCode):
        condition = {'index': indexCode}
        fields = {"_id": 0}

        data = self.mongoObj.getRecords(self.indicesCollection, condition, fields)

        response = []
        for info in data:
            result = {
                "symbol": info['symbol'],
                'name': info['index'],
                'price': info['last_traded_price'],
                'prev_price': info['prevclose'],
            }
            response.append(result)
        return response
