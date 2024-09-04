from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2306221900',
        'name': 'Thorbert Anson Shi',
        'class': 'PBP E'
    }

    return render(request, "main.html", context)
