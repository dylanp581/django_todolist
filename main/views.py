from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item, User, ScheduleItem
from .forms import CreateNewList, ScheduleItemForm
from django.contrib.auth.decorators import login_required


def login_required_with_redirect(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login page with next parameter
            return redirect(f'/login/?next={request.path}')
        return view_func(request, *args, **kwargs)
    return wrapper

def base(response):
    current_user = request.user
    context = {
        'user': current_user,
    }
    return render(request, 'base.html', context)

@login_required_with_redirect
def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():

        if response.method == "POST":
            print(response.POST)
            if response.POST.save:
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False

                    item.save()


            elif response.POST.newItem:
                txt = response.POST.new

                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete = False)
                else:
                    print("invalid")

            elif response.POST.delete:
                del_object = ToDoList.objects.get(id=id)
                del_object.delete()
                return HttpResponseRedirect("/view")

            elif response.POST.delete_item:
                item_id = response.POST.delete_item
                item = Item.objects.get(id=int(item_id))
                item.delete()

        return render(response, "main/list.html", {"ls":ls})
    return render(response, "main/view.html", {})

def home(response):
    return render(response, "main/home.html", {})

@login_required_with_redirect
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

@login_required_with_redirect
def view(response):
    return render(response, "main/view.html", {ToDoList.id:"td.id"})

def fetch_profile(request):
    user = request.user
    user.save()

def profile(response):
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("delete_account"):
            fetch_profile(response)
            return redirect("/home")
    return render(response, "main/profile.html", {})

@login_required_with_redirect
def create_schedule_item(request):
    if request.method == 'POST':
        form = ScheduleItemForm(request.POST)
        if form.is_valid():
            schedule_item = form.save(commit=False)
            schedule_item.user = request.user
            schedule_item.save()
            return redirect('schedule_list')
    else:
        form = ScheduleItemForm()
    return render(request, 'main/create_schedule.html', {'form': form})

@login_required_with_redirect
def schedule_list(request):
    # Order items by the 'order' field
    schedule_items = ScheduleItem.objects.filter(user=request.user).order_by('order')
    return render(request, 'main/schedule_list.html', {'schedule_items': schedule_items})

@login_required_with_redirect
def delete_schedule_item(request, item_id):
    # Get the specific schedule item, ensuring it belongs to the current user
    schedule_item = get_object_or_404(ScheduleItem, id=item_id, user=request.user)

    if request.method == 'POST':
        # Delete the item
        schedule_item.delete()
        return redirect('schedule_list')

    # Render confirmation template
    return render(request, 'main/delete_schedule_item.html', {'item': schedule_item})

@login_required_with_redirect
def schedule_list(request):
    # Order by start time instead
    schedule_items = ScheduleItem.objects.filter(user=request.user).order_by('start_time')
    return render(request, 'main/schedule_list.html', {'schedule_items': schedule_items})

@login_required_with_redirect
def toggle_schedule_item(request, item_id):
    schedule_item = get_object_or_404(ScheduleItem, id=item_id, user=request.user)

    if request.method == 'POST':
        # Toggle the completion status
        schedule_item.is_completed = not schedule_item.is_completed
        schedule_item.save()

    return redirect('schedule_list')