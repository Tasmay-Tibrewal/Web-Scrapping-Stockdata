import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import csv
import os


##Function Definitions Here


#INSTRUCTIONS:-

#to fetch stock information call fetchStock() function

#to fetch top gainers UPDATED information (LIVE) call fetchtop() function,
#exportGainers() will be automatically called within it and gainer.csv will be automatically updated

#to fetch top gainers - NOT UPDATED information directly from gainers.csv file call importGainers() function

#to fetch top losers UPDATED information (LIVE) call fetchloss() function,
#exportLosers() will be automatically called within it and loser.csv will be automatically updated

#to fetch top losers - NOT UPDATED information directly from losers.csv file call importLosers() function

#to export portfolio call addtoPortfolio() function,
#exportPortfolio() will be automatically called within it and Portfolio.csv will be automatically updated

#to fetch news information call Newsletter() function

#to clear Portfolio call clearPortfolio() function

#fetchData() function is automatically called during other functions no need to call it externally

#to fetch Portfolio UPDATED information (LIVE) call refreshPortfolio() function

#to fetch Portfolio - NOT UPDATED information directly from portfolio.csv file call importPortfolio() function

#NOTE- PLEASE CHECK THE STRUCTURE AND DATA TYPE OF RETURN STATEMENT OR FUNCTION ARGUMENTS
#AS MENTIONED BELOW OR IN START OF EACH FUNCTION



def fetchStock(stocks):

    stockData=[]
    stocks=list(stocks.split(','))

    for i in stocks:
            stockData.append(fetchData(nosp(i)))

    return stockData

    #Stock Data is nested list Data Type
    #4 columns- Name, Price(Intraday), Change_pt, Change_%


def nosp(word):
    
    r_word = "";

    for i in word:
    
        if ord(i) in [46,65 ,66 ,67 ,68 ,69 ,70 ,71 ,72 ,73 ,74 ,75 ,76 ,77 ,78 ,79 ,80 ,81 ,82 ,83 ,84 ,85 ,86 ,87 ,88 ,89 ,90]:
            r_word = r_word + i;
    
    return r_word


def fetchtop():

    url='https://finance.yahoo.com/gainers'

    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')

    name= soup.find('tbody').find_all('a')
    name=name[:10]

    dataStock=[]

    for i in name:
        j=str(i)
        x=j.find('>')
        k=j[(x+1):]
        y=k.find('/')
        k=k[:(y-1)]
        dataStock.append(fetchData(k))

    exportGainers(dataStock)

    return dataStock

    #dataStock is in nested list format
    #4 columns- Name, Price(Intraday), Change_pt, Change_%


def fetchloss():

    url='https://finance.yahoo.com/losers'

    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')

    name= soup.find('tbody').find_all('a')
    name=name[:10]

    dataStock=[]

    for i in name:
        j=str(i)
        x=j.find('>')
        k=j[(x+1):]
        y=k.find('/')
        k=k[:(y-1)]
        dataStock.append(fetchData(k))

    exportLosers(dataStock)

    return dataStock

    #dataStock is in nested list format
    #4 columns- Name, Price(Intraday), Change_pt, Change_%


def addtoPortfolio(stockData):

    #stockData has to be in nested list format

    for i in range(len(stockData)):

        inp='Enter the Quantity of '+stockData[i][0]+' :'
        q=float(input(inp).strip())
        p=''

        for j in str(stockData[i][1]):

            if j in ['1','2','3','4','5','6','7','8','9','0','.']:
                p+=j

        amt=q*float(p)
        amt=round(amt,2)

        stockData[i].append(q)
        stockData[i].append(amt)

    exportPortfolio(stockData)


def exportPortfolio(stockData):

    #stockData has to be in nested list format

    with open('portfolio.csv','a',newline='') as csvfile:

        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(stockData)

    print("Portfolio has been updated. ")


def rewritePortfolio(stockData):

    #stockData has to be in nested list format

    with open('portfolio.csv','w',newline='') as csvfile:

        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(stockData)

    print("Portfolio has been updated. ")


def exportGainers(stockData):

    #stockData has to be in nested list format

    with open('gainers.csv','w',newline='') as csvfile:

        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(stockData)


def exportLosers(stockData):

    #stockData has to be in nested list format

    with open('losers.csv','w',newline='') as csvfile:

        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(stockData)


def Newsletter():

    news=[]

    url=f'https://finance.yahoo.com/'

    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')

    head_main = soup.find('h2',{'class':'Fz(22px)--md1100 Lh(25px)--md1100 Fw(b) Tsh($ntkTextShadow) Td(u):h Fz(25px) Lh(31px)'}).text
    news.append(head_main)
    
    news_main= soup.find('p',{'class':'Fz(12px) Fw(n) Lh(14px) LineClamp(3,42px) Pt(6px) Tov(e)'}).text
    news.append(news_main)
    
    url_main= str(soup.find('div',{'class':'Pos(a) B(0) Start(0) End(0) Bg($ntkLeadGradient) Pstart(25px) Pstart(18px)--md1100 Pt(50px) Pend(45px) Pend(25px)--md1100 Bdrsbend(2px) Bdrsbstart(2px)'}))
    
    i=url_main.find('http')
    j=url_main.find('html')
    
    url_main=url_main[i:j+4]
    news.append(url_main)
    
    news_other= soup.find('ul',{'class':'Pos(r) article-cluster-boundary'})
    
    headers=news_other.find_all('h3')
    
    for h3 in headers:
        news.append(h3.text)
    
    links=news_other.find_all('a')
    
    for a in links:
    
        b=str(a)
    
        i=b.find('http')
        j=b.find('html')
    
        b=b[i:j+4]
    
        news.append(b)
    
    return news
    
    #news is list data type and format of news is :-
    # [0] index- Main News title
    # [1] index- Main News in short
    # [2] index- Main News link
    # [3] index- Other News title _ 1st news
    # [4] index- Other News title _ 2nd news
    # [5] index- Other News title _ 3rd news
    # [6] index- Other News link _ 1st news
    # [7] index- Other News link _ 1st news
    # [8] index- Other News link _ 1st news


def refreshPortfolio():
    
    stockData=[]
    l2=[]
    
    with open('portfolio.csv','r',newline='') as csvfile:
    
        csvreader = csv.reader(csvfile)
    
        for row in csvreader:
            l2.append(row)
    
    net=0
    
    for i in l2:
    
        l=(fetchData(i[0]))
        l.append(i[4])
        p=''
    
        for j in str(l[1]):
    
            if j in ['1','2','3','4','5','6','7','8','9','0','.']:
                p+=j
    
        p=float(p)
        amt=float(i[4])*p
        amt=round(amt,2)
    
        l.append(amt)
    
        net+=amt
    
        stockData.append(l)

    rewritePortfolio(stockData)
    
    net=round(net,2)
    stockData.append(net)
    
    return stockData
    
    #stockData in form of nested list, it contains records, and then the net value (total amount of stocks purchased)
    #6 columns- Name, Price(Intraday), Change_pt, Change_%, Quantity, Amount


def importPortfolio():

    l2=[]
    net=0

    with open('portfolio.csv','r',newline='') as csvfile:

        csvreader = csv.reader(csvfile)

        for row in csvreader:

            l2.append(row)
            net+=float(row[5])

    net=round(net,2)
    l2.append(net)

    return l2

    #l2 is in nested list format, it contains records, and then the net value (total amount of stocks purchased)
    #6 columns- Name, Price(Intraday), Change_pt, Change_%, Quantity, Amount


def importGainers():

    l2=[]

    with open('gainers.csv','r',newline='') as csvfile:

        csvreader = csv.reader(csvfile)

        for row in csvreader:
            l2.append(row)

    return l2

    #l2 is in nested list format
    #4 columns- Name, Price(Intraday), Change_pt, Change_%


def importLosers():

    l2=[]

    with open('losers.csv','r',newline='') as csvfile:

        csvreader = csv.reader(csvfile)

        for row in csvreader:
            l2.append(row)

    return l2

    #l2 is in nested list format
    #4 columns- Name, Price(Intraday), Change_pt, Change_%


def clearPortfolio():
    os.remove('portfolio.csv')


def fetchData(symbol):

    #symbol is a string of stock codes

    symbol=symbol.upper()

    url=f'https://finance.yahoo.com/quote/{symbol}'

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' }

    r=requests.get(url, headers=headers)
    soup=BeautifulSoup(r.text, 'html.parser')

    name = symbol

    price = soup.find('fin-streamer',{'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    change_pt = soup.find('div',{'class':'D(ib) Mend(20px)'}).find_all('span')[0].text
    change_per = soup.find('div',{'class':'D(ib) Mend(20px)'}).find_all('span')[1].text

    currency= soup.find('div',{'class':'C($tertiaryColor) Fz(12px)'}).find('span').text
    currency=str(currency)

    i=currency.find('Currency in')

    currency=currency[i+12:]

    value=1.0

    if currency !='USD':

        url2=f'https://finance.yahoo.com/quote/{currency}%3DX?'

        r=requests.get(url2, headers=headers)
        soup=BeautifulSoup(r.text,'html.parser')

        value= soup.find('fin-streamer',{'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
        value=float(value)

    price.strip()
    p=''

    for i in str(price):

            if i in ['1','2','3','4','5','6','7','8','9','0','.']:
                p+=i

    p=float(p)
    price=p/value
    price=round(price,3)

    stock=[name,price,change_pt,change_per]

    return stock

    #Stock is list Data Type
    #4 columns- Name, Price(Intraday), Change_pt, Change_%



##Main Program Begins Here

defaultYes=True

while defaultYes==True:

    action=int(input("What would you like to do today?\n1.Look at stock Data\n2.Top 10 Performers\n3.Top 10 Losers\n4.Check Performance of Portfolio(Updated)\n5.Look at Portfolio (not updated for gui only)\n6.Look at Gainers (not updated for gui only)\n7.Look at Losers (not updated for gui only)\n8.News Letter\n9.Clear Portfolio\n10.Quit\n:: ").strip())

    if action==1:

        stockData=[]
        stocks=input("Enter stocks to search data from. Eg: NVDA,NFLX: ").upper().strip()
        stockData=fetchStock(stocks)

        print("Requesting Data....\nProcessing Information....\n")
        print(tabulate(stockData, headers=["Name", "Price", "Change_pt", "Change_%"]))

        act2=input("Do you want to add to Portfolio? y/n:: ").lower().strip()

        if act2=='y':
            addtoPortfolio(stockData)

    elif action==2:

        stockData=[]

        print("Requesting Data....\nProcessing Information....\n")
        print('Please be patient it may take up to 30 seconds to refresh.')

        stockData=fetchtop()

        print(tabulate(stockData, headers=["Name", "Price(Intraday)", "Change_pt", "Change_%"]))

    elif action==3:

        stockData=[]

        print("Requesting Data....\nProcessing Information....\n")
        print('Please be patient it may take up to 30 seconds to refresh.')

        stockData=fetchloss()

        print(tabulate(stockData, headers=["Name", "Price(Intraday)", "Change_pt", "Change_%"]))

    elif action==4:

        stockData=refreshPortfolio()

        net=stockData[-1]
        stockData=stockData[:-1]

        print(tabulate(stockData, headers=["Name", "Price(Intraday)", "Change_pt", "Change_%","Quantity","Amount"]))
        print('Net Amount =',net)

    elif action==5:

        stockData=importPortfolio()

        net=stockData[-1]
        stockData=stockData[:-1]

        print(tabulate(stockData, headers=["Name", "Price(Intraday)", "Change_pt", "Change_%","Quantity","Amount"]))
        print('Net Amount =',net)

    elif action==6:

        stockData=importGainers()

        print(tabulate(stockData, headers=["Name", "Price(Intraday)", "Change_pt", "Change_%"]))

    elif action==7:

        stockData=importLosers()

        print(tabulate(stockData, headers=["Name", "Price(Intraday)", "Change_pt", "Change_%"]))

    elif action==8:

        news=Newsletter()

        print('\n\nMain News of the Day : \n')

        print(news[0])
        print(news[1],'\n')

        print('Full news link :',news[2],'\n\n')

        print('Other News : \n')

        print(news[3],'\n')
        print('Full news link :',news[6],'\n\n')

        print(news[4],'\n')
        print('Full news link :',news[7],'\n\n')

        print(news[5],'\n')
        print('Full news link :',news[8],'\n\n')

    elif action==9:

        clearPortfolio()

        print('Portfolio is cleared now.')

    elif action==10:
        defaultYes=False

    else:
        print("Wrong Input?! Please Try Again::")

