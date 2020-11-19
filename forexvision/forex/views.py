from django.shortcuts import render, redirect
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
API_KEY3 = "R5jC9C67BMmAwkbGK5rtsY"
API_KEY4 = "Dhd5RG5RAU7CXMJTaTqhAh"
# vishal = taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN
# ravi = meZyuHiwLZxWD1xaBOPfkHtQx4FiWnuhQQMNxsmLQXrL12YveV
# vani = MyQvGNXzWw2DPorALLO1Cet
# vishal2 = R5jC9C67BMmAwkbGK5rtsY
# sanket = Dhd5RG5RAU7CXMJTaTqhAh

base, counter = 0, 0

# Create your views here.
def temp(request):
    return render(request,'Base.html')

def home(request):
    amount = request.POST.get('amount')

    global base
    base = request.POST.get('baseCurr') # get the base currency symbol from user
    global counter
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

    lastUpd = lastUpdated()
    flag = "show"

    context = {'totalAmount' : totalAmount,
                'base' : base, 'counter' : counter,
                'counterrate' : counterrate, 'baserate' : baserate,
                'lastUpd' : lastUpd,
                'flag' : flag
              }
    return render(request,'Base.html',context)

def lastUpdated():
    json_url = urlopen("https://fcsapi.com/api-v3/forex/latest?symbol="+base+"/"+counter+"&access_key="+API_KEY1)
    data = json.loads(json_url.read())

    return data['response'][0]['tm']


def charts(request):
    today = date.today()
    todayDate = today.strftime("%Y-%m-%d")
    fromDate = today - timedelta(days = 365)

    # https://fcsapi.com/api-v2/forex/history?symbol=EUR/USD&period=1d&from=2020-05-01T12:00&to=2020-11-11T12:00&access_key=taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN
    D_json_url = urlopen("https://fcsapi.com/api-v2/forex/history?symbol="+base+"/"+counter+"&period=1d&from="+str(fromDate)+"T12:00&to="+todayDate+"T12:00&access_key="+API_KEY2)
    D_data = json.loads(D_json_url.read())

    dt = D_data['response']

    D_close = []
    D_date = []
    D_high = []
    D_low = []
    count = 0

    for ls in dt:
        if count >= len(dt) - 30:
            D_high.append(ls['h'])
            D_low.append(ls['l'])

        D_close.append(ls['c'])
        D_date.append(ls['tm'][0:10])
        count += 1

    D_fig = plot([Scatter(x=D_date, y=D_close,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='blue')],
               output_type='div')

    D_High = max(D_high)
    D_Low = min(D_low)

    M_fig = M_chart(todayDate, fromDate)
    W_fig = W_chart(todayDate, fromDate)
    return render(request,'Charts.html',{'D_fig' : D_fig, 'D_High' : D_High, 'D_Low' : D_Low,
                          'M_fig' : M_fig, 'W_fig' : W_fig})

def M_chart(todayDate, fromDate):
    M_json_url = urlopen("https://fcsapi.com/api-v2/forex/history?symbol="+base+"/"+counter+"&period=month&from="+str(fromDate)+"T12:00&to="+todayDate+"T12:00&access_key="+API_KEY3)
    M_data = json.loads(M_json_url.read())

    dt = M_data['response']

    M_close = []
    M_date = []

    for ls in dt:
        M_close.append(ls['c'])
        M_date.append(ls['tm'][0:10])

    M_fig = plot([Scatter(x=M_date, y=M_close,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='blue')],
               output_type='div')

    return M_fig

def W_chart(todayDate, fromDate):
    W_json_url = urlopen("https://fcsapi.com/api-v2/forex/history?symbol="+base+"/"+counter+"&period=1w&from="+str(fromDate)+"T12:00&to="+todayDate+"T12:00&access_key="+API_KEY4)
    W_data = json.loads(W_json_url.read())
    dt = W_data['response']

    W_close = []
    W_date = []

    for ls in dt:
        W_close.append(ls['c'])
        W_date.append(ls['tm'][0:10])

    W_fig = plot([Scatter(x=W_date, y=W_close,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='blue')],
               output_type='div')

    return W_fig

