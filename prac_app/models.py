from django.db import models
import re # regex

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')


# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}

        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="invalid email address."

        if len(postData['first_name']) < 3:
            errors['first_name']="First Name must be more than 2 characters."

        if len(postData['last_name']) < 3:
            errors['last_name']="Last Name must be more than 2 characters."

        if len(postData['password']) < 3:
            errors['password']="Password must be more than 8 characters."

        if postData["password"] != postData["confirm_password"]:
            errors['password']="Passwords must match."

        for user in User.objects.all():
            if postData['email'] == user.email:
                errors['email'] = 'Email is already in our database'
                break
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=60)
    last_name=models.CharField(max_length=60)
    first_name=models.CharField(max_length=60)
    email=models.CharField(max_length=60)
    password=models.CharField(max_length=60)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # wish
    # likes
    objects= UserManager()



class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors={}

        if len(postData['item']) < 3:
            errors['item']="wish must be more than 3 characters."
       
        if len(postData['desc']) < 3:
            errors['desc']="description must be more than 3 characters."

        return errors
    



class Wish(models.Model):
    item=models.CharField(max_length=60)
    desc=models.TextField(max_length=500)
    granted=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # relationships
    users_who_wished=models.ForeignKey('User',related_name='wish',on_delete=models.CASCADE)
    users_who_liked=models.ManyToManyField('User',related_name='likes')
    objects= WishManager()


