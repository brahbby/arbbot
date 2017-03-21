import httplib
import urllib
import json
import hashlib
import hmac
from pprint import pprint
import csv 
#import pyexcel_ods
import numpy as np
import requests
import collections
import poloniex
from array import *
import re
import logging
import time
#from pyexcel_ods import save_data
t0 = time.time()
polo = poloniex.Poloniex()

#Price Dictionary emptry creation
pricedict = {}

#coinpairs
#coin1 = 'btc'
#print 'Coin 1 %s' % coin1
#coin2 = 'eth'
#print 'Coin 2 %s' % coin2
def bot(coin1,coin2):   #coin 1 = market coin2  = alt
    #Poloniex Pair
    polo1 = coin1 + '_' + coin2
    polopair = polo1.upper()
    print polopair
    
    #C-cex pair
    ccexpair = coin2 + '-' + coin1
    print ccexpair
    
    #Yobitpair
    yobitpair = coin2 + '_' + coin1
    print yobitpair
    
    # get Poloniex Orderbook
    pricedict['polo'] = polo.api('returnOrderBook', {'currencyPair':polopair})
    print 'Polo Bids/Buys'
    print pricedict['polo']['bids'][0]
    print 'Polo Asks/Sells'
    print pricedict['polo']['asks'][0]
    
    #Get C-Cex Orderbook
    ordertype = 'both' 				#can be buy,sell or both
    orderdepth = '5'                  #how many orders to pull
    puburl = 'https://c-cex.com/t/api_pub.html?a=getorderbook&market='
    url1 = str(puburl+ccexpair+'&type='+ordertype+'&depth='+orderdepth) #api url to string
    orderdata1 = requests.get(url1)          #get json data from website
    ccex = orderdata1.json()
    pricedict['ccex'] = ccex
    
    print '-----------'
    print 'C-cex Sell'
    print pricedict['ccex']['result']['sell'][0]
    print 'C-cex Buy'
    print pricedict['ccex']['result']['buy'][0]
    
    #Get YObit Prices
    puburl = 'https://yobit.net/api/3/depth/'
    url = str(puburl+yobitpair) #api url to string
    #print url
    orderdata = requests.get(url)          #get json data from website
    #print orderdata
    yobitorders = orderdata.json()
    
    
    print '-----------'
    pricedict['yobit'] = yobitorders[yobitpair]
    print 'YoBit Bids/Buys'
    print pricedict['yobit']['bids'][0]
    print 'YoBit Asks/Sells'
    print pricedict['yobit']['asks'][0]
    
    print 'Ccex->YoBit'
    ccexbuy = pricedict['ccex']['result']['sell'][0]['Rate']#*pricedict['ccex']['result']['sell'][0]['Quantity']
    print 'ccex buy price'
    print ccexbuy
    yobitsell = pricedict['yobit']['bids'][0][0] #*pricedict['yobit']['bids'][0][1]
    print 'yobit sell price'
    print yobitsell
    pricediff = yobitsell-ccexbuy
    print 'Pricediff'
    print pricediff
    print 'Profit pct'
    profit = (pricediff/ccexbuy)*100
    print profit
    minvol = min(pricedict['ccex']['result']['sell'][0]['Quantity'],pricedict['yobit']['bids'][0][1])
    print 'minvol'
    print minvol
    btcprofit = pricediff * minvol
    print 'BTC profit'
    print btcprofit
    print '-------------'
    print 'YoBit->Ccex'
    
    yobitbuy = pricedict['yobit']['asks'][0][0] #*pricedict['yobit']['bids'][0][1]
    print 'yobit buy price'
    print yobitbuy
    ccexsell = pricedict['ccex']['result']['buy'][0]['Rate']#*pricedict['ccex']['result']['sell'][0]['Quantity']
    print 'ccex sell price'
    print ccexsell
    
    pricediff = ccexsell-yobitbuy
    print 'Pricediff'
    print pricediff
    print 'Profit pct'
    profit = (pricediff/yobitbuy)*100
    print profit
    minvol = min(pricedict['ccex']['result']['buy'][0]['Quantity'],pricedict['yobit']['asks'][0][1])
    print 'minvol'
    print minvol
    btcprofit = pricediff * minvol
    print 'BTC profit'
    print btcprofit
    
def getmarkets():
    marketdict = {}
    marketdict = polo.api('returnTicker')
    print marketdict