from fastapi import FastAPI, Body
from stockDetails_payload import StockDetails
from typing import Annotated
from StockInfo import  StockInfo

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