from django.urls import path
from . import views
urlpatterns = [
    #Create
    path('books/add/', views.add_book),
    #Read
    path('books/', views.books),
    #Read
    path('books/my_books/', views.my_books),
    #Read
    path('books/detail/<int:book_id>/', views.book),
    #Update
    path('books/update/<int:book_id>/', views.update_book),
    #Update
    path('books/favorite/<int:book_id>/', views.favorite_book),
    #Update
    path('books/unfavorite/<int:book_id>/', views.unfavorite_book),
    #Delete
    path('books/delete/<int:book_id>/', views.del_book),
]
