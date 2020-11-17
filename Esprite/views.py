from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import SignupForm


class HomePageView(TemplateView):
    template_name = "home/homepage.html"


class LoginView(FormView):
    template_name = "login/login.html"
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('product:list')
            else:
                errors = form.errors['__all__']
                return render(request, self.template_name, {'form': form, 'errors': errors})


class LogoutView(FormView):
    template_name = "logout/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('product:list')
