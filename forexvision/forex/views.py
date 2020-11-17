from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
import json
from datetime import date,timedelta
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter

API_KEY = "taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN"
API_KEY1 = "meZyuHiwLZxWD1xaBOPfkHtQx4FiWnuhQQMNxsmLQXrL12YveV"
API_KEY2 = "MyQvGNXzWw2DPorALLO1Cet"
# vishal = taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN
# ravi = meZyuHiwLZxWD1xaBOPfkHtQx4FiWnuhQQMNxsmLQXrL12YveV
# vani = MyQvGNXzWw2DPorALLO1Cet


# Create your views here.
def temp(request):
    return render(request,'Base.html')

def home(request):
    amount = request.POST.get('amount')

    base = request.POST.get('baseCurr') # get the base currency symbol from user
    counter = request.POST.get('counterCurr') # get the counter currency symbol from user

    # # Check if the base and counter is not none
    # # After requesting the server and getting data from user

    json_url = urlopen("https://fcsapi.com/api-v2/forex/converter?pair1="+base+"&pair2="+counter+"&amount="+amount+"&access_key="+API_KEY)
    data = json.loads(json_url.read())

    baseindex = "price_1x_"+base
    counterindex = "price_1x_"+counter

    baserate = data['response'][baseindex]
    counterrate = data['response'][counterindex]
    totalAmount = data['response']['total']

    lastUpd = lastUpdated(base, counter)
    High, Low, lineGraph = graph(base, counter)

    flag = "show"

    context = {'totalAmount' : totalAmount,
                'base' : base, 'counter' : counter,
                'counterrate' : counterrate, 'baserate' : baserate,
                'lastUpd' : lastUpd,
                'High' : High, 'Low' : Low,
                'lineGraph' : lineGraph,
                'flag' : flag
             }
    return render(request,'Base.html',context)

def lastUpdated(base, counter):
    json_url = urlopen("https://fcsapi.com/api-v3/forex/latest?symbol="+base+"/"+counter+"&access_key="+API_KEY1)
    data = json.loads(json_url.read())

    return data['response'][0]['tm']

def graph(base, counter):

    today = date.today()
    todayDate = today.strftime("%Y-%m-%d")
    fromDate = today - timedelta(days = 365)

    # https://fcsapi.com/api-v2/forex/history?symbol=EUR/USD&period=1d&from=2020-05-01T12:00&to=2020-11-11T12:00&access_key=taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN
    json_url = urlopen("https://fcsapi.com/api-v2/forex/history?symbol="+base+"/"+counter+"&period=1d&from="+str(fromDate)+"T12:00&to="+todayDate+"T12:00&access_key="+API_KEY2)
    data = json.loads(json_url.read())

    dt = data['response']

    close = []
    tareek = []
    high = []
    low = []
    count = 0

    for ls in dt:
        if count >= len(dt) - 30:
            high.append(ls['h'])
            low.append(ls['l'])

        close.append(ls['c'])
        tareek.append(ls['tm'][0:10])
        count += 1

    fig = plot([Scatter(x=tareek, y=close,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='blue')],
               output_type='div')
    return max(high), min(low), fig