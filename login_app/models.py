from django.db import models
import re	# the regex module
import bcrypt   # must install in virtual environment: pip install bcrypt
from time import gmtime, strftime
from datetime import datetime
from dateutil.relativedelta import *   # must install in virtual environment: pip install python-dateutil
from dateutil.parser import *    # must install in virtual environment: pip install python-dateutil
import pytz    # must install in virtual environment: 

class UserManager(models.Manager):
    def basic_validator(self, postData, user_status):
        errors = {}

        if 'id' in postData:
            user_id = postData['id']
        else:
            user_id = 0

        ALPHA_REGEX = re.compile(r'^[a-zA-Z]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if user_status == 'new':
            if not ALPHA_REGEX.match(postData['first_name']):
                errors["first_name"] = "First name must be alpha characters only."
            elif len(postData['first_name']) < 2:
                errors["first_name"] = "First name must be at least 2 alpha characters."
            if not ALPHA_REGEX.match(postData['last_name']):
                errors["last_name"] = "Last name must be alpha characters only."
            elif len(postData['last_name']) < 2:
                errors["last_name"] = "Last name must be at least 2 alpha characters."
            if postData['birth_date'] == "":
                errors["birth_date"] = "Birth Date must be populated."
            elif postData['birth_date'] > datetime.now().strftime("%Y-%m-%d"):
                errors["birth_date"] = "Birth Date must be in the past."
            elif relativedelta(datetime.now(), isoparse(postData['birth_date'])).years < 13:
                errors["birth_date"] = "Birth Date must be at least 13 years old."
            if not EMAIL_REGEX.match(postData['email_address']):
                errors["email_address"] = "Email address provided for registration is not valid."
            elif len(User.objects.filter(email_address=postData['email_address']).exclude(id=user_id)) > 0:
                errors['email_address'] = "Email address for registration must be unique."
            if len(postData['password1']) < 8:
                errors["password1"] = "Password provided for registration must be at least 8 characters."
            elif postData['password1'] != postData['password2']:
                errors["password1"] = "Password fields provided for registration are not the same."
        elif user_status == 'old':
            if not EMAIL_REGEX.match(postData['email_address_login']):
                errors["email_address_login"] = "Email address provided for login is not valid."
            elif len(User.objects.filter(email_address=postData['email_address_login'])) == 0:
                errors['email_address_login'] = "An account for this email address does not exist."
            elif len(postData['password1']) < 8:
                errors["password1"] = "Password provided for login must be at least 8 characters."
            else:
                user = User.objects.filter(email_address=postData['email_address_login'])
                logged_user = user[0]
                if not bcrypt.checkpw(postData['password1'].encode(), logged_user.password.encode()):
                    errors['password1']  = "The password provided for login was incorrect!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"