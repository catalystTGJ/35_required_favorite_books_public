from django.shortcuts import HttpResponse, render, redirect
from django.db.models.functions import Lower
from django.contrib import messages
from .models import Books
from login_app.models import User

#DRY
def user_check(request, expected):
    if 'user_id' in request.session and request.method == expected:
        user = user = User.objects.get(id=int(request.session['user_id']))
    else:
        user = ""
    return user

#DRY
def assemble_context_render(request, user, htmldoc, book_id=0, errors={}):
    for key, value in errors.items():
        messages.error(request, value)
    if htmldoc == "books.html":
        if 'title' in request.POST:
            title = request.POST['title']
            description = request.POST['description']
        else:
            title = ""
            description = ""
        context = {
            'user' : user,
            'new_book' : {'title': title, 'description': description},
            'books' : Books.objects.all().annotate(utitle=Lower('title')).order_by('utitle')
        }
    elif htmldoc == "my_books.html":
        context = {
            'user' : user,
            'books' : User.objects.first().favorite_books.all().annotate(utitle=Lower('title')).order_by('utitle')

        }
    elif htmldoc == "book.html":
        context = {
            'user' : user,
            'book' : Books.objects.get(id=book_id)
        }
    return render(request, htmldoc, context)

#Create
def add_book(request):
    user = user_check(request, "POST")
    if user:
        errors = Books.objects.basic_validator(request.POST, status="new")
        if len(errors) == 0:
            this_book = Books.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                owner_id = user.id
            )
            this_book.users_who_like.add(user)
            return redirect (f"/books/detail/{this_book.id}")
        else:
            return assemble_context_render(request, user=user, htmldoc="books.html", errors=errors)
    return redirect ("/books")

#Read
def books(request):
    user = user_check(request, "GET")
    if user:
        return assemble_context_render(request, user=user, htmldoc="books.html")
    return redirect ("/")

#Read
def my_books(request):
    user = user_check(request, "GET")
    if user:
        return assemble_context_render(request, user=user, htmldoc="my_books.html")
    return redirect ("/")


#Read
def book(request, book_id):
    user = user_check(request, "GET")
    if user:
        return assemble_context_render(request, user=user, htmldoc="book.html", book_id=book_id)
    return redirect ("/books")

#Update
def update_book(request, book_id):
    user = user_check(request, "POST")
    if user:
        errors = Books.objects.basic_validator(request.POST, status="old")
        if len(errors) == 0:
            this_book = Books.objects.get(id=book_id)
            this_book.title = request.POST['title']
            this_book.description = request.POST['description']
            this_book.save()
            return redirect(f"/books/detail/{book_id}/")
        else:
            return assemble_context_render(request, user=user, htmldoc="book.html", book_id=book_id, errors=errors)
    return redirect ("/books")

def favorite_book(request, book_id):
    user = user_check(request, "POST")
    if user:
        this_book = Books.objects.get(id=book_id)
        this_book.users_who_like.add(user)
        return redirect (request.POST['return_to'])
    return redirect ("/books")

def unfavorite_book(request, book_id):
    user = user_check(request, "POST")
    if user:
        this_book = Books.objects.get(id=book_id)
        this_book.users_who_like.remove(user)
        return redirect (request.POST['return_to'])
    return redirect ("/books")

#Delete
def del_book(request, book_id):
    user = user_check(request, "POST")
    if user:
        errors = Books.objects.basic_validator(request.POST, status="delete")
        if len(errors) == 0:
            this_book = Books.objects.get(id=book_id)
            this_book.delete()
            return redirect ("/books")
        else:
            return assemble_context_render(request, user=user, htmldoc="book.html" , book_id=book_id, errors=errors)
    return redirect ("/books")
