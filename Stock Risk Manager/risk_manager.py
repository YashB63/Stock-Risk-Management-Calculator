import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import statistics
import time
import matplotlib.pyplot as plt

yf.pdr_override() # activate yahoo finance workaround
now = dt.datetime.now() # Runs until today's date
start = dt.datetime(2023,1,1)

avg_gain = 17 # Enter your average gain
avg_loss = 6 # Enter your average loss
sma_used = [50,200]
ema_used = [21]

stock = input("enter the stock symbol (enter 'quit' to stop): ") # query user for stock ticker
while stock != "quit": # ye loop tab tk chalega jb tk user 'quit' na type kar de (can do many stocks in a row)
    
    df = pdr.get_data_yahoo(stock,start,now)
    close = df["Adj Close"][-1]
    max_stop = close*((100-avg_loss)/100)
    one_risk_target = round(close*((100+avg_gain)/100),2) # 1 risk target
    two_risk_target = round(close*((100+(2*avg_gain))/100),2) # 2 risk target
    three_risk_target = round(close*((100+(3*avg_gain))/100),2) # 3 risk target
    
    # lets check
    
    # print(str(max_stop))
    # print(str(one_risk_target))
    # print(str(two_risk_target))
    # print(str(three_risk_target))
    
    for x in sma_used:
        sma = x
        df["SMA_" + str(sma)] = round(df.iloc[:,4].rolling(window=sma).mean(),2)
    for x in ema_used:
        ema = x
        df['EMA_' + str(ema)] = round(df.iloc[:,4].ewm(span=ema,adjust=False).mean(),2)
        
    sma50 = round(df["SMA_50"][-1],2)
    sma200 = round(df["SMA_200"][-1],2)
    ema21 = round(df["EMA_21"][-1],2)
    low5 = round(min(df["Low"].tail(5)),2)
    
    percentage_from_50_sma = round(((close/sma50)-1)*100,2)
    check50 = df["SMA_50"][-1]>max_stop #percentage from the 50 days is greater than max_stop value
    
    percentage_from_200_sma = round(((close/sma200)-1)*100,2)
    check200 = ((close/df["SMA_200"][-1])-1)*100>100
    
    percentage_from_21_ema = round(((close/ema21)-1)*100,2)
    check21 = df["EMA_21"][-1]>max_stop
    
    percentage_low = round(((close/low5)-1)*100,2)
    checkl = percentage_low>max_stop# checklow
    
    print()
    print("Current Stock: " +stock+" Price: "+str(round(close,2)))
    print("21 EMA: "+str(ema21)+ " | 50 SMA: "+str(sma50)+" | 200 SMA: "+str(sma200)+" | 5 day Low: "+str(low5))
    print("------------------------------------------------")
    print("Max Stop: "+str(round(max_stop,2)))
    print("Price Targets: ")
    print("One Risk Target: "+str(one_risk_target))
    print("Two Risk Target: "+str(two_risk_target))
    print("Three Risk Target: "+str(three_risk_target))
    print("From 5 day Low "+ str(percentage_low)+ "% -Within Max stop: "+str(checkl))
    print("From 21 day EMA "+ str(percentage_from_21_ema)+ "% -Within Max stop: "+str(check21))
    print("From 50 day SMA "+ str(percentage_from_50_sma)+ "% -Within Max stop: "+str(check50))
    print("From 200 day SMA "+ str(percentage_from_200_sma)+ "% -In Danger Zone (Over 100% from 200 SMA): "+str(check200))
    print()
    
        
    
    stock = input("Enter the stock symbol (enter 'quit' to stop): ") # query user for next stock