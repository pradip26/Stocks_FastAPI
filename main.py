from fastapi import FastAPI, Body
from stockDetails_payload import StockDetails
from typing import Annotated
from StockInfo import  StockInfo
from ResultEnum import ResultInfo

app = FastAPI()

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
    resultData = stockinfoObj.getResultDetails(resultinfo.symbol.upper(),resultinfo.result_type)
    return resultData