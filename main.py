from fastapi import FastAPI, Body
from stockDetails_payload import StockDetails
from typing import Annotated
from StockInfo import  StockInfo
from ResultEnum import ResultInfo
from fastapi.middleware.cors import CORSMiddleware
import datetime

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
async def create_item(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    stockdata = stockinfoObj.getStockDetails(stockdetails.symbol.upper())
    return stockdata

@app.post("/priceDetails/")
async def create_item(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    priceData = stockinfoObj.getPriceDetails(stockdetails.symbol.upper())
    return priceData

@app.post("/resultDetails/")
async def create_item(resultinfo: Annotated[ResultInfo,Body(embed=True)]):
    stockinfoObj = StockInfo()
    resultData = stockinfoObj.getResultDetails(resultinfo.symbol.upper(),resultinfo.result_type.value)
    return resultData

@app.post("/corpActions/")
async def create_item(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    corpActionsData = stockinfoObj.getCorpActions(stockdetails.symbol.upper())
    return corpActionsData

@app.post("/histPrices/")
async def create_item(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    current_date = datetime.date.strftime(datetime.datetime.today(), "%Y-%m-%d")
    previous_date = datetime.date.strftime( (datetime.datetime.today() - datetime.timedelta(days=60)),"%Y-%m-%d")
    histPriceData = stockinfoObj.getHistPirces(stockdetails.symbol.upper(), previous_date, current_date)
    return histPriceData

@app.post("/peersList/")
async def create_item(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    histPriceData = stockinfoObj.getPeersList(stockdetails.industry)
    return histPriceData

@app.post("/topScoresList/")
async def create_item():
    stockinfoObj = StockInfo()
    scoreData = stockinfoObj.getTopScoreStockList()
    return scoreData

@app.post("/getScore/")
async def create_item(stockdetails: Annotated[StockDetails,Body(embed=True)]):
    stockinfoObj = StockInfo()
    scoreData = stockinfoObj.getStockScore(stockdetails.symbol.upper())
    scoreData = list(scoreData)[0]
    return scoreData