from django.db import models
from time import gmtime, strftime
from datetime import datetime
import pytz    # must install in virtual environment: 
from login_app.models import User


class BooksManager(models.Manager):
    def basic_validator(self, postData, status):
        errors = {}

        if 'book_id' in postData:
            book_id = int(postData['book_id'])
        else:
            book_id = 0

        if status == "new" or status == "old":
            if len(postData['title']) == 0:
                errors["title"] = "A Title must be at least 1 character."
            elif len(Books.objects.filter(title=postData['title']).exclude(id=book_id)) > 0:
                errors['title'] = "A Title must be unique."
            if len(postData['description']) < 5:
                errors["description"] = "Description must be at least 5 characters."
        elif status == "delete":
            if Books.objects.get(id=book_id).owner_id != int(postData['user_id']):
                errors["owner_id"] = "Only the user who initially uploaded a book may remove a book."
        return errors

class AuthorsManager(models.Manager):
    def basic_validator(self, postData, status):
        errors = {}

        if 'author_id' in postData:
            author_id = int(postData['author_id'])
        else:
            author_id = 0

        if status == "new" or status == "old":
            if len(postData['first_name']) < 2:
                errors["first_name"] = "First name must be at least 2 characters."
            if len(postData['last_name']) < 2:
                errors["last_name"] = "Last name must be at least 2 characters."
            if len(postData['notes']) < 5:
                errors["notes"] = "Notes must be at least 5 characters."
        elif status == "delete":
            if Authors.objects.get(id=author_id).owner_id != int(postData['user_id']):
                errors["owner_id"] = "Only the user who initially uploaded an author may remove an author."
        return errors

class PublishersManager(models.Manager):
    def basic_validator(self, postData, status):
        errors = {}

        if 'publisher_id' in postData:
            publisher_id = int(postData['publisher_id'])
        else:
            publisher_id = 0

        if status == "new" or status == "old":
            if len(postData['name']) < 2:
                errors["name"] = "Name must be at least 2 characters."
            if len(postData['notes']) < 5:
                errors["notes"] = "Notes must be at least 5 characters."
        elif status == "delete":
            if Authors.objects.get(id=publisher_id).owner_id != int(postData['user_id']):
                errors["owner_id"] = "Only the user who initially uploaded a publisher may remove a publisher."
        return errors

class Books(models.Model):
    owner = models.ForeignKey(User, related_name="user_books", on_delete=models.DO_NOTHING)
    users_who_like = models.ManyToManyField(User, related_name="favorite_books")
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BooksManager()

class Authors(models.Model):
    owner = models.ForeignKey(User, related_name="user_authors", on_delete=models.DO_NOTHING)
    users_who_like = models.ManyToManyField(User, related_name="favorite_authors")
    books_authored_by = models.ManyToManyField(Books, related_name="authors")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorsManager()
    @property
    def full_name(self):
        return f"{first_name} {last_name}"

class Publishers(models.Model):
    owner = models.ForeignKey(User, related_name="user_publishers", on_delete=models.DO_NOTHING)
    users_who_like = models.ManyToManyField(User, related_name="favorite_publishers")
    books_published_by = models.ManyToManyField(Books, related_name="publishers")
    name = models.CharField(max_length=255)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PublishersManager()


