orderbookDepths = [.05, .5]

def initPoloConnection():
   from poloniex import Poloniex
   return Poloniex()
      

def getCoinNames():
   api = initPoloConnection()
   coinList = []
   coins = api.return24hVolume()
   for market in coins:
      if "BTC_" in market:
         coinList.append(market)
   return coinList      
      

def getBidDepthRatio(orderbook):
   bids, asks = [orderbook["bids"], orderbook["asks"]]
   price = (float(bids[0][0]) + float(asks[0][0])) / 2
   totalBidVol = sum([float(bid[1]) * float(bid[0]) for bid in bids])
   volsAtDepths = [totalBidVol * orderbookDepths[0], totalBidVol * orderbookDepths[1]]
   secondLevel = False
   bidVol = 0
   pricesAtDepths = []
   for bid in bids:
      if (not secondLevel) and bidVol >= volsAtDepths[0]:
         pricesAtDepths.append(float(bid[0]))
         secondLevel = True
     
      if secondLevel and bidVol >= volsAtDepths[1]:
         pricesAtDepths.append(float(bid[0]))
         break
         
      bidVol += float(bid[1]) * float(bid[0])
   pricesAtDepthsRatio = pricesAtDepths[0]/pricesAtDepths[1]
   return pricesAtDepthsRatio
   
   
def getAskDepthRatio(orderbook):
   bids, asks = [orderbook["bids"], orderbook["asks"]]
   price = (float(bids[0][0]) + float(asks[0][0])) / 2
   totalAskVol = sum([float(ask[1]) * price for ask in asks])
   volsAtDepths = [totalAskVol * orderbookDepths[0], totalAskVol * orderbookDepths[1]]
   secondLevel = False
   askVol = 0
   pricesAtDepths = []
   for ask in asks:
      if (not secondLevel) and askVol >= volsAtDepths[0]:
         pricesAtDepths.append(float(ask[0]))
         secondLevel = True
     
      if secondLevel and askVol >= volsAtDepths[1]:
         pricesAtDepths.append(float(ask[0]))
         break
         
      askVol += float(ask[1]) * price
   pricesAtDepthsRatio = pricesAtDepths[1]/pricesAtDepths[0]
   return pricesAtDepthsRatio


def getCoinDepthRatio(pair):
   api = initPoloConnection()
   orderbook = api.returnOrderBook(pair, depth=10000000)
   bidDepthRatio = getBidDepthRatio(orderbook)
   askDepthRatio = getAskDepthRatio(orderbook)
   averageDepthRatio = askDepthRatio * bidDepthRatio
   return averageDepthRatio
   
def getAllCoinDepthRatios():
   coinRatios = {}
   coinNames = getCoinNames()
   for coin in coinNames:
      coinRatios[coin] = getCoinDepthRatio(coin)
   return coinRatios
   
def printAllCoinRatios():
   from operator import itemgetter
   allCoinRatios = getAllCoinDepthRatios()
   for coin in sorted(allCoinRatios.items(), key=itemgetter(1)):
      print(coin[0].replace("BTC_", "").lower() + ": " + str(allCoinRatios[coin[0]]))
  

if __name__ == "__main__":
   printAllCoinRatios()
