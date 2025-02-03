from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form":form})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        user = authenticate(request, username=username, password1=password1, password2=password2)
        if user is not None:
            login(request, user)
            return redirect("/home")
    else:
        return redirect("/login")

    return render(request, "login.html", {})

def logout_user(request):
    # logout(request)
    # return redirect("/home")
    return HttpResponse("<h1>hello</h1>")