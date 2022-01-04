from django.shortcuts import render


# Тестова ф-я для отдачи главной
def main(request):
    return render(request, 'mainapp/index.html')
