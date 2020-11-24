import logging
from itertools import chain

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, logout, login


from convertimage.models import ImageUnit

log = logging.getLogger(__name__)

class LoginPage(View):
    def get(self, request):
        log.info(f"is user authenticated? {request.user.is_authenticated}")
        if request.user.is_authenticated is True:
            return redirect('dashboard')
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
    # def associate_images(self, ):

class DashboardPage(View):
    def get(self, request):
        if request.user.is_authenticated is True:
            session_rel_img = request.session['related_images']
            session_rel_img = ImageUnit.objects.filter(pk__in=session_rel_img)
            user_rel_img = ImageUnit.objects.filter(submitted_by=request.user).order_by("-submitted")
            # Set to remove duplicates, chain to concat session images and user images
            related_images = set(chain(session_rel_img, user_rel_img))

            context = {
                'related_images': related_images,
            }
            return render(request, 'dashboard.html', context)
        else:
            return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('home')