import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, logout, login

log = logging.getLogger(__name__)

class LoginPage(View):
    def get(self, request):
        log.info(f"is user authenticated? {request.user.is_authenticated}")
        if request.user.is_authenticated is True:
            return redirect('home')
        else:
            return render(request, 'login.html')
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html')
        else:
            login(request, user)
            return redirect('dashboard')

class DashboardPage(View):
    def get(self, request):
        if request.user.is_authenticated is True:
            return render(request, 'dashboard.html')
        else:
            return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('home')