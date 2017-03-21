from poloniex import Poloniex
from ccex import ccex
from yobit import yobit


class arbbot:
    cc = ccex()
    polo = Poloniex()
    yb = yobit()
    #print polo.marketTicker()
    
    #---------------------------------------------------------------------
    #Get coins listed and buy sell prices
    def poloticker():
        polodata = polo.marketTicker() #get ticker data + prices + markets
        polodict = {} #set empty dict for polo values
        #print polodata 
        for key,value in polodata.items():
            polodict[key] = [value['highestBid'],value['lowestAsk']] #add market as key (buy,sell)
            #print key
            #print value['highestBid']
            #print value['lowestAsk']
        print polodict
    
    
    def ccexticker():
        ccexdata = cc.prices()
        ccexdict = {}
        #print ccexdata
        for key,value in ccexdata.items():
            ccexdict[key] = [value['buy'],value['sell']] #add market as key (buy,sell)
            #print key
            #print value['buy']
            #print value['sell']
        print ccexdict
       
       
       
    def yobitticker():
       #initialize lists/vars
        ybpairs = []
        ybcall = ''
        ybdict = {}
        
        #get list of pairs from yobit
        yobitdata = yb.info()['pairs']
        for key, value in yobitdata.items(): 
            ybpairs.append(key)
        print ybpairs
        
        count = 0
        for tickers in ybpairs:
            #ybcall = ybcall + tickers +'-'
    
            if count <58:     #max yobit API call = 59 pairs
                ybcall = ybcall + tickers +'-'    # add dash after pair
                count+=1
            else:
                ybdata = yb.marketTicker(ybcall[:-1])
                print '---------------------------------------------------------'
                for key,value in ybdata.items():
                    ybdict[key] = [value['buy'],value['sell']] #add market as key (buy,sell)
                ybcall = ''
                count = 0
           
            
        print ybdict

            
    def getmarkets():
        poloticker()
        ccexticker()
        ybticker()

getmarkets()
#print polo.marketOrders('BTC_LTC')
