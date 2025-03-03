from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item, User
from .forms import CreateNewList
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.

def base(response):
    current_user = request.user
    context = {
        'user': current_user,
    }
    return render(request, 'base.html', context)

def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():

        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False

                    item.save()


            elif response.POST.get("newItem"):
                txt = response.POST.get("new")

                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete = False)
                else:
                    print("invalid")

            elif response.POST.get("delete"):
                del_object = ToDoList.objects.get(id=id)
                del_object.delete()
                return HttpResponseRedirect("/view")
            
            elif response.POST.get("delete_item"):
                item_id = response.POST.get("delete_item")
                item = Item.objects.get(id=int(item_id))
                item.delete()

        return render(response, "main/list.html", {"ls":ls})
    return render(response, "main/view.html", {})

def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()

            if response.user.is_authenticated:
                response.user.todolist.add(t)

        return HttpResponseRedirect("/%i" %t.id)    

    else:
        form = CreateNewList()

    return render(response, "main/create.html", {"form": form})

def view(response):
    return render(response, "main/view.html", {ToDoList.id:"td.id"})

def fetch_profile(request):
    user = request.user
    user.delete()

def profile(response):
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("delete_account"):
            fetch_profile(response)
            return redirect("/home")
    return render(response, "main/profile.html", {})