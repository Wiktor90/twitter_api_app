from django.shortcuts import render

def main(request):
    return render(request, 'FPL_tw/main.html')
