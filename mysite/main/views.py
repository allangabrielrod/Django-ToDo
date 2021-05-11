from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.

from .models import ToDoList, Item
from .forms import CreateNewList


def index(response, id):
    todo = ToDoList.objects.get(id=id)

    if todo in response.user.todolist.all():

        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in todo.item_set.all():
                    if(response.POST.get("c" + str(item.id))) == 'clicked':
                        item.complete = True
                    else:
                        item.complete = False

                    item.save()

            elif response.POST.get("newItem"):
                text = response.POST.get("new")

                if len(text) > 2:
                    todo.item_set.create(text=text, complete=False)
                else:
                    print('Invalid input.')

        return render(response, 'main/list.html', {'todo': todo})
    return render(response, 'main/view.html', {})


def home(response):
    return render(response, 'main/home.html')


def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            todo = ToDoList(name=name)
            todo.save()
            response.user.todolist.add(todo)

        return HttpResponseRedirect("/%i" % todo.id)

    else:
        form = CreateNewList()

    return render(response, 'main/create.html', {'form': form})


def view(response):
    return render(response, 'main/view.html', {})
