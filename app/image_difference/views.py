import logging

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import User

from convertimage.models import ImageUnit

from .forms import LoginForm, SignupForm

log = logging.getLogger(__name__)

class LoginPage(View):
    def setup(self, request, *args, **kwargs):
        # Make sure the session has a list of related images, even if it's empty
        if request.session.get('related_images', None) is None:
            request.session['related_images'] = list()
        super(LoginPage, self).setup(request, *args, **kwargs)

    def get(self, request):
        log.info(f"is user authenticated? {request.user.is_authenticated}")
        if request.user.is_authenticated is True:
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'login_form': LoginForm(), "signup_form": SignupForm()})
    def post(self, request):
        if request.POST["type"] == "login":
            return self._login(request)
        else:
            return self._signup(request)

    def _login(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'login.html', {'login_form': LoginForm(), "signup_form": SignupForm()})
            else:
                login(request, user)
                session_rel_img = request.session['related_images']
                self.associate_images(session_rel_img, user)
                return redirect('dashboard')
        else:
            return render(request, 'login.html', {'login_form': LoginForm(), "signup_form": SignupForm()})

    def _signup(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            log.info(form.cleaned_data)
            username = form.cleaned_data["username"]
            email    = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            session_rel_img = request.session['related_images']
            self.associate_images(session_rel_img, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'login_form': LoginForm(), "signup_form": SignupForm()})

    @staticmethod
    def associate_images(session_rel_images, user):
        session_rel_images = ImageUnit.objects.filter(pk__in=session_rel_images, submitted_by__exact=None)
        for image in session_rel_images:
            image.submitted_by = user
            image.save()

class DashboardPage(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated is True:
            user_rel_img = ImageUnit.objects.filter(submitted_by=request.user).order_by("-submitted")

            context = {
                'related_images': user_rel_img,
            }
            return render(request, 'dashboard.html', context)
        else:
            return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('home')