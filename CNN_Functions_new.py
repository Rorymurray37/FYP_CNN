import pandas as pd
import tensorflow as tf
from keras.models import Sequential
from sklearn.metrics import confusion_matrix


def buy(df,bal,holdings,priceindex,tradelength,tradeAmount):
    
    close = df.columns.get_loc("Close") # get index of close col
    buyindex = priceindex
    sellindex = priceindex+tradelength #sell price 100 timesteps forward
    
    buyprice = df.iloc[buyindex,close]
    shares = tradeAmount/buyprice
    shares = int(shares)
    buytotal = shares*buyprice
    
 
    
    bal = bal - buytotal #10 shares bought
        
    

    #buytotal = 10 * buyprice

    
    #print("buyprice : ",buyprice," sell : ",sellprice , "pl ",(sellprice-buyprice)/buyprice)
    
   
    newposition = Position(buyindex,sellindex,shares)
    
    return bal,holdings,newposition
              



def BuyHold(df):

    #Buy & Hold
    balance = 100000

    close = df.columns.get_loc("Close")
    buyamount = 100000/df.iloc[0,close]
    buyamount = int(buyamount)
    buy = buyamount*df.iloc[0,close]

    sell = buyamount *df.iloc[-1,close]

    diff = sell - buy
    pl = diff/buy *100
    pl = int(pl)
    print('P&L : ',pl,'%')




def sell(bal,holdings,price,amount):
    
    selltotal = amount*price
    bal = bal + selltotal

        
    return bal,holdings

def sellall(bal,holdings,price,shares):
    total = shares * price
    holdings = 0
    bal = total
    shares = 0
    return bal,holdings


class Position:
    def __init__(self, buyindex, sellindex,amount):
        
        self.buyindex = buyindex
        self.sellindex = sellindex
        self.amount = amount
      

    def get_sellprice(self):
        return sellprice
        
    def get_buyprice(self):
        return buyindex



# Paper Trade
#works buy buying when label 1, balance is updated and a new position object is created until the
#position is finally closed

def paperTrade(df,tradelength,tradeAmount):
    
    balance = 100000
    stockholdings = 0
    numShares = 0
    Labelcol = df.columns.get_loc("Label") # get index of label col
    close = df.columns.get_loc("Close")
    goodtrades = 0
    numTrades = 0 
    averagepl = 0


    buylist = []  #list to store buy positions 

    for i in range(len(df)):
        if df.iloc[i,Labelcol] == 1:
            if balance > tradeAmount  and i+tradelength<len(df):
                
                balance,stockholdings,position = buy(df,balance,stockholdings,i,tradelength,tradeAmount)
                
                #print(balance)
                buylist.append(position)
                
                
                
                
                
        
        
    
        if len(buylist) != 0:  #buylist not empty 
            for t in buylist:
                pos = t
                sellindex = pos.sellindex #get buy and sell indexes for the position
                buyindex  = pos.buyindex 
                sharesAmount = pos.amount
            
                if(i >= sellindex):
                    numTrades = numTrades+1 #increase trade count
                    sellprice = df.iloc[i,close] #get buy and sell prices
                    buyprice = df.iloc[buyindex,close]
                    
                    balance,stockholdings = sell(balance,stockholdings,sellprice,sharesAmount) #sell the stock
                    pl = (sellprice-buyprice)/buyprice 
                    pl = pl*100
                    
                    if(pl>0): #check if pl is positive
                        goodtrades = goodtrades+1
                        averagepl = averagepl +pl
                        
                    buylist.remove(pos)
                    del pos
                
                
                
    print(len(buylist))               
    balance = float(str(round(balance, 2))) #rounding 
    stockholdings = float(str(round(stockholdings,2))) 
 

    print('Final balance : ',balance)   #print outputs
    print('Final holdings : ', stockholdings)
    print('Number of profitable trades ',goodtrades,'/',numTrades)
    if goodtrades>0:
        print('Average P&L for profitable trades : ',averagepl/goodtrades,'%')
    pl =  balance - 100000
    pl_percentage = pl/100000 *100
    print( "P&L : ", pl,'  Gain : ',pl_percentage,'%' )
    
    filename = 'JUNE.txt'
    f = open(filename,'a')
    print('Final balance : ',balance, file=f)
    print('Final holdings : ', stockholdings,file=f)
    print('Trade length : ', tradelength,' Trade amount :',tradeAmount,file=f)
    print('Number of profitable trades ',goodtrades,'/',numTrades,file=f)
    if goodtrades>0:
        print('Average P&L for profitable trades : ',averagepl/goodtrades,'%',file=f)
    print( "P&L : ", pl,'  Gain : ',pl_percentage,'%' ,file=f)
    print('-----------------------------------------------------',file=f)
    print(' ',file=f)
    f.close()


def scale(df,df_test):
    from sklearn.preprocessing import MinMaxScaler
    import pandas as pd

    mm_scaler = MinMaxScaler(feature_range=(0, 1))

    mm_scaler.fit(df.values)
    df_test = pd.DataFrame(mm_scaler.transform(df_test.values),columns=df_test.columns, index=df_test.index)
    df = pd.DataFrame(mm_scaler.transform(df.values), columns=df.columns, index=df.index)

    return df,df_test


def create_images(df, n_steps):
    from numpy import array
    X, y = list(), list()
    for i in range(len(df)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the dataset
        if end_ix > len(df):
            break
        # gather input and output parts of the pattern
        seq_x ,seq_y= df.iloc[i:end_ix, :-1], df.iloc[end_ix-1, -1]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


def Test(model,testx,testy,df,window_size = 15):
    results = model.evaluate(testx, testy)
    predictions = model.predict(testx)
    
    newpred = []
    for i in range(len(predictions)):
        if predictions[i][0] < 0.5:
            newpred.append(0)
        
        else:
            newpred.append(1)
    
    confusion = confusion_matrix(testy, newpred)
    m = predictions.max()
    print('Confusion Matrix', confusion) 

    print("test loss, test acc:", results) 
    print('Max prediction ' ,m)
 
    filename = 'JUNE.txt'
    f = open(filename,'a')
    
    print('Tested on : ',df.name,file=f)
    print("test loss, test acc:", results,file=f) 
    print('Max prediction ' ,m,file=f)
    print(' ',file=f)
    f.close()



    cnn_pred = pd.DataFrame(columns = ['Close', 'Label'])


    for i in range(len(testx)):
        if(i+window_size<len(df)):

            if predictions[i] > 0.5:
                cnn_pred = cnn_pred.append({'Close' : df.iloc[i+window_size,3] , 'Label' : 1}, ignore_index = True)
            else:
                cnn_pred = cnn_pred.append({'Close' : df.iloc[i+window_size,3] , 'Label' : 0}, ignore_index = True)

    return cnn_pred
