from django.shortcuts import render


def home(request):
    """home view
    :input: - request
    :return: - render template home.html
    """
    return render(request, 'home.html')