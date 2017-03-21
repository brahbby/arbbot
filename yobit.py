import httplib
import urllib
import json
import hashlib
import hmac
import requests
import time
from datetime import datetime

#Yobit API
#Mike Dunn 3/16/17

minute = 60
hour = minute*60
day = hour*24
week = day*7
month = day*30
year = day*365

# Possible Commands
PUBLIC_COMMANDS = ['info', 'depth','marketTicker','trades'] 
PRIVATE_COMMANDS = ['returnBalances', 'returnCompleteBalances', 'returnDepositAddresses', 'generateNewAddress', 'returnDepositsWithdrawals', 'returnOpenOrders', 'returnTradeHistory', 'returnAvailableAccountBalances', 'returnTradableBalances', 'returnOpenLoanOffers', 'returnActiveLoans', 'createLoanOffer', 'cancelLoanOffer', 'toggleAutoRenew', 'buy', 'sell', 'cancelOrder', 'moveOrder', 'withdraw', 'transferBalance', 'returnMarginAccountSummary', 'marginBuy', 'marginSell', 'getMarginPosition', 'closeMarginPosition']

nonce = 0 #need to setup fiel for nonce storage/import

class yobit:
    def __init__(self, APIKey='', Secret=''):
        self.APIKey = APIKey
        self.Secret = Secret
        # Conversions
        self.timestamp_str = lambda timestamp=time.time(), format="%Y-%m-%d %H:%M:%S": datetime.fromtimestamp(timestamp).strftime(format)
        self.str_timestamp = lambda datestr=self.timestamp_str(), format="%Y-%m-%d %H:%M:%S": int(time.mktime(time.strptime(datestr, format)))
        self.float_roundPercent = lambda floatN, decimalP=2: str(round(float(floatN)*100, decimalP))+"%"
        
        	#PUBLIC COMMANDS
        self.info = lambda x=0: self.api('info')
        self.depth = lambda x=0: self.api('depth')
        self.marketTicker = lambda coinpair: self.api('ticker/%s'%coinpair)
        self.trades = lambda x=0: self.api('trades')

        
        #PRIVATE COMMANDS
        #self.myTradeHist = lambda pair: self.api('returnTradeHistory',{'currencyPair':pair})
        self.myAvailBalances = lambda x=0: self.api('returnAvailableAccountBalances')
        self.myMarginAccountSummary = lambda x=0: self.api('returnMarginAccountSummary')
        self.myMarginPosition = lambda pair='all': self.api('getMarginPosition',{'currencyPair':pair})
        self.myCompleteBalances = lambda x=0: self.api('returnCompleteBalances')
        self.myAddresses = lambda x=0: self.api('returnDepositAddresses')
        self.myOrders = lambda pair='all': self.api('returnOpenOrders',{'currencyPair':pair})
        self.myDepositsWithdraws = lambda x=0: self.api('returnDepositsWithdrawals')
        self.myTradeableBalances = lambda x=0: self.api('returnTradableBalances')
        self.myActiveLoans = lambda x=0: self.api('returnActiveLoans')
        self.myOpenLoanOrders = lambda x=0: self.api('returnOpenLoanOffers')
        ## Trading functions ##
        self.createLoanOrder = lambda coin, amount, rate: self.api('createLoanOffer', {'currency' :coin, 'amount':amount, 'duration':2, 'autoRenew':0, 'lendingRate':rate})
        self.cancelLoanOrder = lambda orderId: self.api('cancelLoanOffer', {'orderNumber':orderId})
        self.toggleAutoRenew = lambda orderId: self.api('toggleAutoRenew', {'orderNumber':orderId})
        self.closeMarginPosition = lambda pair: self.api('closeMarginPosition',{'currencyPair':pair})
        self.marginBuy = lambda pair, rate, amount, lendingRate=2: self.api('marginBuy',{'currencyPair':pair, 'rate':rate, 'amount':amount, 'lendingRate':lendingRate})
        self.marginSell= lambda pair, rate, amount, lendingRate=2: self.api('marginSell',{'currencyPair':pair, 'rate':rate, 'amount':amount, 'lendingRate':lendingRate})
        self.buy = lambda pair, rate, amount: self.api('buy', {'currencyPair':pair, 'rate':rate, 'amount':amount})
        self.sell = lambda pair, rate, amount: self.api('sell', {'currencyPair':pair, 'rate':rate, 'amount':amount})
        self.cancelOrder = lambda orderId: self.api('cancelOrder', {'orderNumber':orderId})
        self.moveOrder = lambda orderId, rate, amount: self.api('moveOrder', {'orderNumber':orderId, 'rate':rate, 'amount':amount})
        self.withdraw = lambda coin, amount, address: self.api('withdraw', {'currency':coin, 'amount':amount, 'address':address})
        self.transferBalance = lambda coin, amount, fromac, toac: self.api('transferBalance', {'currency':coin, 'amount':amount, 'fromAccount':fromac, 'toAccount':toac})
        
    	#####################
	# Main Api Function #
	#####################
    def api(self, command, args={}):
        """
        returns 'False' if invalid command or if no APIKey or Secret is specified (if command is "private")
        returns {"error":"<error message>"} if API error
        """
        args['command'] = command
        #if command in PRIVATE_COMMANDS:
        #    pass
        #elif command in PUBLIC_COMMANDS:
        url = 'https://yobit.net/api/3/'
        #print command
        #if not args:
        ret = requests.get(url + command)
        #print url + command
        #print ret
        return ret.json()
        #else:
            #ret = requests.get(url + command)#urlencode(args))
            #print ret
            #return ret.json()
        #else:return False




