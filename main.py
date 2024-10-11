from fastapi import FastAPI, Body
from stockDetails_payload import StockDetails
from typing import Annotated
from StockInfo import StockInfo
from ResultEnum import ResultInfo
from fastapi.middleware.cors import CORSMiddleware
import datetime
from indexDetails_payload import IndexDetails
from IndicesInfo import IndexInfo


app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async  def root():
    return {"message":"welcome to api"}

@app.post("/stocksdetails/")
async def stocks_details(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    stockdata = stockinfoObj.getStockDetails(stockdetails.symbol.upper())
    return stockdata

@app.post("/priceDetails/")
async def stock_price_data(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    priceData = stockinfoObj.getPriceDetails(stockdetails.symbol.upper())
    return priceData

@app.post("/resultDetails/")
async def stocks_results(resultinfo: Annotated[ResultInfo,Body(embed=True)]):
    stockinfoObj = StockInfo()
    resultData = stockinfoObj.getResultDetails(resultinfo.symbol.upper(),resultinfo.result_type.value)
    return resultData

@app.post("/corpActions/")
async def corporate_actions(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    corpActionsData = stockinfoObj.getCorpActions(stockdetails.symbol.upper())
    return corpActionsData

@app.post("/histPrices/")
async def historical_prices(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    current_date = datetime.date.strftime(datetime.datetime.today(), "%Y-%m-%d")
    previous_date = datetime.date.strftime( (datetime.datetime.today() - datetime.timedelta(days=60)),"%Y-%m-%d")
    histPriceData = stockinfoObj.getHistPirces(stockdetails.symbol.upper(), previous_date, current_date)
    return histPriceData

@app.post("/peersList/")
async def stocks_peers_list(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    histPriceData = stockinfoObj.getPeersList(stockdetails.industry)
    return histPriceData

@app.post("/topScoresList/")
async def top_stocks_in_score_list():
    stockinfoObj = StockInfo()
    scoreData = stockinfoObj.getTopScoreStockList()
    return scoreData

@app.post("/getScore/")
async def score_data(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    scoreData = stockinfoObj.getStockScore(stockdetails.symbol.upper())
    scoreData = list(scoreData)[0]
    return scoreData

@app.get("/getSamplePortfolio/")
async def list_model_pf(type: str = "sample"):
    stockinfoObj = StockInfo()
    pfData = stockinfoObj.getSamplePF(type)
    return pfData

@app.get("/getSampleLatestPortoflioValue/")
async def latest_sample_pf_value(type: str = "sample"):
    stockinfoObj = StockInfo()
    pfData = stockinfoObj.getSampleLatestPortfolioData(type)
    return pfData

@app.get("/getSamplePortfolioWeeklyGraph/")
async def sample_portfolio_weekly_graph(type: str = "sample"):
    stockinfoObj = StockInfo()
    pfData = stockinfoObj.getSamplePortfolioWeeklyGraph(type)
    return pfData

@app.post("/getCandleGraphData/")
async def getCandleGraphData(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    current_date = datetime.date.strftime(datetime.datetime.today(), "%Y-%m-%d")
    previous_date = datetime.date.strftime((datetime.datetime.today() - datetime.timedelta(days=stockdetails.days)), "%Y-%m-%d")
    histData = stockinfoObj.getHistPirces(stockdetails.symbol.upper(), previous_date, current_date)
    stockMovingAverages = stockinfoObj.getStockMovingAverages(stockdetails.symbol.upper())
    print(stockMovingAverages)
    response = []
    for data in histData:
        mvData = stockMovingAverages[data['date']]
        mv20 = round(float(mvData["mv_20"]),2)
        mv100 = round(float(mvData['mv_100']),2)
        mv200 = round(float(mvData['mv_200']),2)
        newData = data
        newData["mv_20"] = mv20
        newData["mv_100"] = mv100
        newData["mv_200"] = mv200
        response.append(newData)

    return response

@app.post("/indicesHistPrices/")
async def indexHistPrices(IndexDetails: Annotated[IndexDetails,Body(embed=True)]):
    indexInfoObj = IndexInfo()
    stockdata = indexInfoObj.getHistPirces(IndexDetails.indexcode.upper())
    return stockdata

@app.post("/stockVSIndexGraph/")
async def stockVSndexGraphData(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    current_date = datetime.date.strftime(datetime.datetime.today(), "%Y-%m-%d")
    previous_date = datetime.date.strftime((datetime.datetime.today() - datetime.timedelta(days=stockdetails.days)), "%Y-%m-%d")
    histData = stockinfoObj.getHistPirces(stockdetails.symbol.upper(), previous_date, current_date)

    indexInfoObj = IndexInfo()
    indexHistdata = indexInfoObj.getHistPirces("NIFTY 50", previous_date, current_date)

    stockIistDataWithIndex = indexInfoObj.indexCalculations(histData)
    indexHistDataWithIndexVal = indexInfoObj.indexCalculations(indexHistdata)

    response = {}
    list = []
    for data in stockIistDataWithIndex:
        dt = data['date']
        price = data['price']
        indexVal = data['index']
        response[dt] = {
            'date': dt,
            'stock_price': price,
            'stock_index_val': round(indexVal,2)
        }

    for indexdata in indexHistDataWithIndexVal:
        dt = indexdata['date']
        price = indexdata['price']
        indexVal = round(indexdata['index'],2)
        if dt in response.keys():
            response[dt].update({'index_price':price,'index_val':indexVal})

    for fd in response.values():
        list.append(fd)
    return list

@app.post("/getIndexDetails/")
async def getIndexDetails(IndexDetails: Annotated[IndexDetails,Body(embed=True)]):
    indexInfoObj = IndexInfo()
    indexData = indexInfoObj.getIndexDetails(IndexDetails.indexcode.upper())
    return indexData