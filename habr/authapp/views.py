# from django.shortcuts import render, HttpResponseRedirect
# from django.urls import reverse
# from authapp.forms import UserRegisterForm
#
#
# def register(request):
#     title = 'Регистрация'
#
#     if request.method == 'POST':
#         register_form = UserRegisterForm(request.POST, request.FILES)
#
#         if register_form.is_valid():
#             register_form.save()
#             return HttpResponseRedirect(reverse('auth:login'))
#
#     else:
#         register_form = UserRegisterForm()
#
#     content = {'title': title, 'register_form': register_form}
#
#     return render(request, 'authapp/register.html', content)
