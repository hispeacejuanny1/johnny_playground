from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def number_bingo(request):
    return render(request, 'games/number_bingo.html')
