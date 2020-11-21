from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate

class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated is True:
            return redirect ('home')
        return render(request, 'login.html')
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse("failed to login")
        else:
            return redirect('home')

class DashboardPage(View):
    def get(self, request):
        if request.user.is_authenticated is True:
            return HttpResponse("dashboard")
        else:
            return HttpResponse("denied")
