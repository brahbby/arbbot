from poloniex import Poloniex
from ccex import ccex
from yobit import yobit



cc = ccex()
polo = Poloniex()
yb = yobit()
#print polo.marketTicker()

#---------------------------------------------------------------------
#Get coins listed and buy sell prices
def poloticker():
    polodata = polo.marketTicker() #get ticker data + prices + markets
    polodict = {} #set empty dict for polo values
    for key,value in polodata.items():
        polodict[key] = [value['highestBid'],value['lowestAsk']] #add market as key (buy,sell)
    return polodict


def ccexticker():
    ccexdata = cc.prices()
    ccexdict = {}
    for key,value in ccexdata.items():
        ccexdict[key] = [value['buy'],value['sell']] #add market as key (buy,sell)
    return ccexdict
   
   
   
def yobitticker():
   #initialize lists/vars
    ybpairs = []
    ybcall = ''
    ybdict = {}
    
    #get list of pairs from yobit
    yobitdata = yb.info()['pairs']
    
    #create list of pairs called ybapirs
    for key, value in yobitdata.items(): 
        ybpairs.append(key)
    #intialize count for counting pairs
    count = 0 
    #print ybpairs
    for tickers in ybpairs:
        if count <58:     #max yobit API call = 59 pairs
            ybcall = ybcall + tickers +'-'    # add dash after pair and append to string of 
            count+=1                          #increment count
        #after 57th pari, call yobit price api
        else:         
            ybdata = yb.marketTicker(ybcall[:-1])     #subract last dash from string of 
            for key,value in ybdata.items():
                ybdict[key] = [value['buy'],value['sell']] #add market as key (buy,sell)
            ybcall = ''
            count = 0
       
        
    return ybdict




#print polo.marketOrders('BTC_LTC')
