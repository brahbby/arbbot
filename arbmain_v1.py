import arbbotclass_v2 as ab


#Polo to yobit pair format
def poloconv(pair,direction):
    if direction == 'to':
        dash =  pair.find('_')
        pair = (pair[(dash+1):len(pair)]+pair[dash]+pair[0:dash]).upper()
    elif direction == 'from':
        dash =  pair.find('_')
        pair = (pair[(dash+1):len(pair)]+pair[dash]+pair[0:dash]).lower()
    else:
        print 'Poloconv: Direction or coin needed'
    return pair
    
#ccex to yobit pair format
def ccexconv(pair,direction):
    if direction == 'to':
        pair = pair.replace('_','-')
    elif direction == 'from':
        pair = pair.replace('-','_')
    else:
        print 'Ccexconv: Direction or coin needed'
    return pair
        
        
def getmarkets():
    #init price dictionary
    pricedict = {}
    
    #get polo prices and convert to yobit format
    polodata = ab.poloticker()
    for key,value in polodata.items():
        key = poloconv(key,'from')
        try:
            pricedict[key].append({'polo':[value[0],value[1]]}) #append prices to single dict 0 = buy; 1 = sell
        except KeyError:
            pricedict[key] = {'polo':[value[0],value[1]]} #append prices to single dict 0 = buy; 1 = sell
            
    #get polo prices and convert to yobit format    
    ccdata = ab.ccexticker()
    for key,value in ccdata.items():
        key = ccexconv(key,'from')
        try:
            pricedict[key]['ccex'] = [value[0],value[1]] #append prices to single dict 0 = buy; 1 = sell
        except KeyError:
            pricedict[key] = {'ccex':[value[0],value[1]]} #append prices to single dict 0 = buy; 1 = sell
        
    ybdata = ab.yobitticker()
    for key,value in ybdata.items():
        try:
            pricedict[key]['yobit'] = [value[0],value[1]] #append prices to single dict 0 = buy; 1 = sell
        except KeyError:
            pricedict[key] = {'yobit':[value[0],value[1]]} #append prices to single dict 0 = buy; 1 = sell
    return pricedict
    
print getmarkets()
test = getmarkets()

#for key,value in test.items():
    #print key
    #print value
print 'eth'
print test['eth_btc']