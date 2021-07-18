from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# LOGIN PORTION
class UserManager(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        if len(post_data['street_address']) < 2:
            errors['street_address'] = 'Street address must be at least 2 characters'

        if len(post_data['zip_code']) != 5:
            errors['zip_code'] = 'Zipcode must be 5 characters long'

        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid Email Address'
        
        email_check = self.filter(email=post_data['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if post_data['password'] != post_data['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, post_data):
        pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = post_data['first_name'],
            last_name = post_data['last_name'],
            street_address = post_data['street_address'],
            zip_code = post_data['zip_code'],
            email = post_data['email'],
            password = pw,
        )
    def updateme(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        if len(post_data['street_address']) < 2:
            errors['street_address'] = 'Street address must be at least 2 characters'

        # if len(post_data['zip_code']) != 5:
        #     errors['zip_code'] = 'Zipcode must be 5 characters long'

        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid Email Address'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    zip_code = models.IntegerField(max_length=5)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    objects = UserManager()


class InvitedManager(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        if len(post_data['street_address']) < 2:
            errors['street_address'] = 'Street address must be at least 2 characters'

        if len(post_data['zip_code']) != 5:
            errors['zip_code'] = 'Zipcode must be 5 characters long'

        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid Email Address'
        
        email_check = self.filter(email=post_data['email'])
        if email_check:
            errors['email'] = "Email already in use"
        
        return errors
    def invited_user(self, post_data):
        return self.create(
            first_name = post_data['first_name'],
            last_name = post_data['last_name'],
            street_address = post_data['street_address'],
            zip_code = post_data['zip_code'],
            email = post_data['email'],
    )

class Invited(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    zip_code = models.IntegerField(max_length=5)
    email = models.EmailField(unique=True)

    objects = InvitedManager()
# BLOG PORTION

class BlogManager(models.Manager):
    def post_validator(self, postData):
        errors = {}

        if len(postData['title']) < 1:
            errors['title'] = "The title must be at least 3 characters long."
        if len(postData['p_text']) < 10:
            errors['p_text'] = "Post must be at least 10 characters long."

        return errors

class Blogpost(models.Model):
    title = models.CharField(max_length=255)
    b_text = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="has_created_post", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="user_liked_post")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = BlogManager()

# Marketplace PORTION

class ItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}

        if len(postData['brand']) < 1:
            errors['brand'] = "The brand name cannot be empty."
        if len(postData['product_name']) < 1:
            errors['product_name'] = "The product name cannot be empty."
        if len(postData['price']) < 1:
            errors['price'] = "The price cannot be empty."
        if len(postData['description']) < 1:
            errors['description'] = "The description name cannot be empty."
        if len(postData['contact_info']) < 1:
            errors['contact_info'] = "The contact information cannot be empty."

        # if postData['price'] == 0:
        #     errors['price'] = "The price cannot be $0."

        if len(postData['brand']) < 2:
            errors['brand'] = "The brand name must be at least 2 characters long."
        if len(postData['product_name']) < 8:
            errors['product_name'] = "Product name must be at least 8 characters long."
        if len(postData['description']) >50:
            errors['description'] = "The description must be less than 50 characters long."

        return errors

class Item(models.Model):
    product_name = models.CharField(max_length=45)
    item_description = models.CharField(max_length=50)
    item_price = models.IntegerField(max_length=8)
    contact_info = models.CharField(max_length=255)
    item_brand = models.CharField(max_length=45)
    owner = models.ForeignKey(User, related_name="has_created_item", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = ItemManager()