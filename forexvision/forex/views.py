from django.shortcuts import render, redirect
from django.http import HttpResponse
from urllib.request import urlopen
import json
from datetime import date,timedelta
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter
from .models import forex_hours,Trader, Spread
from datetime import datetime
import pytz
import calendar


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
    # if request.method=="POST":
    if request.POST.get('region'):
        radio=request.POST.get('region')
        print(radio)#radio should be like colm name
        trader = Trader.objects.filter(region =radio)
        print(trader)
        return render(request,'Base.html',{'trader':trader})
    else:
        trader = Trader.objects.all()
        return render(request,'Base.html',{'trader':trader})

def home(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        global base
        base = request.POST.get('baseCurr') # get the base currency symbol from user
        global counter
        counter = request.POST.get('counterCurr') # get the counter currency symbol from user

        # # Check if the base and counter is not none
        # # After requesting the server and getting data from user
        json_url = urlopen("https://fcsapi.com/api-v2/forex/converter?pair1="+base+"&pair2="+counter+"&amount="+amount+"&access_key="+API_KEY4)
        data = json.loads(json_url.read())
        if(data['status'] == False):
            print("Wait for 1 min")
            return render(request, 'Base.html')
        else:
            baseindex = "price_1x_"+base
            counterindex = "price_1x_"+counter

            baserate = data['response'][baseindex]
            counterrate = data['response'][counterindex]
            totalAmount = data['response']['total']

            # lastUpd = lastUpdated()
            flag = "show"

            # dt = M_data['response']

            json_urlupd = urlopen("https://fcsapi.com/api-v3/forex/latest?symbol="+base+"/"+counter+"&access_key="+API_KEY1)

            dataupd = json.loads(json_urlupd.read())
            if(dataupd['status'] == False):
                return render(request, 'Base.html', {'lastUpd' : None})
            else:
                ans = abcd(request, base, counter)
                context = {'totalAmount' : totalAmount,
                            'base' : base, 'counter' : counter,
                            'counterrate' : counterrate, 'baserate' : baserate,
                            'lastUpd' : dataupd['response'][0]['tm'],
                            'flag' : flag, 'trader' : ans
                         }

                return render(request,'Base.html',context)

def abcd(request, base, counter):
    if request.POST.get('compare'):
        value = base+counter  # value given by base n counter string concatenation
        check_list = []
        check_list = request.POST.getlist('check[]')
        print("list :", check_list)
        trader = Trader.objects.filter(id__in =check_list)
        spread = Spread.objects.filter(id__in =check_list)
        print(trader)
        # trader = Trader.objects.all()
        # spread = Spread.objects.all()
        ans = list(trader.values())
        ans1 = list(spread.values())
        currency = base+counter

        for i in range(len(ans)):
            ans[i]["spread"] = ans1[i][value]

        return ans
        # return render(request, 'Base.html', {'trader': ans})
    else:
        trader = Trader.objects.all()
        spread = Spread.objects.all()
        ans = list(trader.values())
        ans1 = list(spread.values())
        currency = base+counter

        for i in range(len(ans)):
            ans[i]["spread"] = ans1[i][currency]

        print(ans)

        return ans
        # return render(request, 'Base.html', {'trader': ans})


def charts(request):
    today = date.today()
    todayDate = today.strftime("%Y-%m-%d")
    fromDate = today - timedelta(days = 365)

    # https://fcsapi.com/api-v2/forex/history?symbol=EUR/USD&period=1d&from=2020-05-01T12:00&to=2020-11-11T12:00&access_key=taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN
    D_json_url = urlopen("https://fcsapi.com/api-v2/forex/history?symbol="+base+"/"+counter+"&period=1d&from="+str(fromDate)+"T12:00&to="+todayDate+"T12:00&access_key="+API_KEY2)
    D_data = json.loads(D_json_url.read())

    M_fig = M_chart(todayDate, fromDate)
    W_fig = W_chart(todayDate, fromDate)

    if D_data['status'] == False or M_fig == 'status failed' or W_fig == 'status failed':
        return render(request,'Base.html')
    else:
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
                            # labels = {'x' : 'Time Stamp', 'y' : 'Counter Currency Range'},
                            mode='lines+markers', name='test',
                            opacity=0.8, marker_color='blue')],
                output_type='div')

        D_High = max(D_high)
        D_Low = min(D_low)

        return render(request,'Charts.html',{'base' : base, 'counter' : counter, 'D_fig' : D_fig, 'D_High' : D_High, 'D_Low' : D_Low,
                            'M_fig' : M_fig, 'W_fig' : W_fig})

def M_chart(todayDate, fromDate):
    M_json_url = urlopen("https://fcsapi.com/api-v2/forex/history?symbol="+base+"/"+counter+"&period=month&from="+str(fromDate)+"T12:00&to="+todayDate+"T12:00&access_key="+API_KEY3)
    M_data = json.loads(M_json_url.read())

    if M_data['status'] == False:
        return "status failed"
    else:
        dt = M_data['response']

        M_close = []
        M_date = []

        for ls in dt:
            M_close.append(ls['c'])
            M_date.append(ls['tm'][0:10])


        M_fig = plot([Scatter(x=M_date, y=M_close,
                            # labels = {'x' : 'Time Stamp', 'y' : 'Counter Currency Range'},
                            mode='lines+markers', name='test',
                            opacity=0.8, marker_color='blue')],
                output_type='div')

        return M_fig

def W_chart(todayDate, fromDate):
    W_json_url = urlopen("https://fcsapi.com/api-v2/forex/history?symbol="+base+"/"+counter+"&period=1w&from="+str(fromDate)+"T12:00&to="+todayDate+"T12:00&access_key="+API_KEY4)
    W_data = json.loads(W_json_url.read())

    if W_data['status'] == False:
        return "status failed"
    else:
        dt = W_data['response']

        W_close = []
        W_date = []

        for ls in dt:
            W_close.append(ls['c'])
            W_date.append(ls['tm'][0:10])

        W_fig = plot([Scatter(x=W_date, y=W_close,
                            # labels = {'x' : 'Time Stamp', 'y' : 'Counter Currency Range'},
                            mode='lines+markers', name='test',
                            opacity=0.8, marker_color='blue')],
                output_type='div')

        return W_fig

def market(request):
    Countrydict = {
            'Sydney, Australia' : 'Australia/Sydney',
            'Tokyo, Japan' : 'Japan',
            'Hong Kong, China' : 'Asia/Hong_Kong',
            'Shanghai, China' : 'Asia/Shanghai',
            'Singapore, Singapore' : 'Asia/Singapore',
            'India' : 'Asia/Kolkata',
            'Moscow, Russia' : 'Europe/Moscow',
            'Frankfurt, Germany' : 'Europe/Zurich',
            'Zurich, Switzerland' : 'Europe/Zurich',
            'Paris, France' : 'Europe/Paris',
            'London, United Kingdom' : 'Europe/London',
            'Johannesburg, South Africa' : 'Africa/Johannesburg',
            'New York, United States' : 'America/New_York',
            'Toronto, Canada' : 'America/Toronto',
            'Chicago, United States' : 'America/Chicago'}
    forexs = forex_hours.objects.all()

    countryTZDict = {}
    for i in range(len(forexs)):
        OTime = int(forex_hours.objects.values('open_time')[i]['open_time'][0:2])
        CTime = int(forex_hours.objects.values('close_time')[i]['close_time'][0:2])
        values = forex_hours.objects.values('country_name')[i]['country_name']
        date = str(datetime.now(pytz.timezone(Countrydict[values])))
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        hour = int(date[11:13])
        weekday = calendar.weekday(year, month, day)
        lst = []
        lst.append(date[0:19])
        if(weekday == 5 or weekday == 6):
            lst.append('Close')
            # countryTZDict[values] = 'Close'
        else:
            if hour < OTime or hour > CTime:
                lst.append('Close')
                # countryTZDict[values] = 'Close'
            else:
                lst.append('Open')
                # countryTZDict[values] = 'Open'
        countryTZDict[values] = lst
        print(countryTZDict[values])

    return render(request, 'Market.html', {'forexs': forexs, 'countryTZDict' : countryTZDict })

