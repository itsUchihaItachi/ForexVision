from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    amount = request.POST.get('amount')
    base = request.POST.get('value')
    counter = request.POST.get('value')
    if amount == None :
        amount = 0
    return render(request,'base.html',{'amount' : amount, 'base' : base})

# def page_objects(request):
#     if request.method == 'POST':
#         form = YourForm(request.POST)

#     if form.is_valid():
#         answer = form.cleaned_data['value']

#     return render(request, 'base.html', {'answer' : answer})

