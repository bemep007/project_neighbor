from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import Invited, User, Blogpost, Item, Question



# LOGIN portion of the app.
def index(request):
    return render(request, 'index.html')

def index_authorized(request):
    context ={
        'all_posts': Blogpost.objects.all().order_by('created_at')[:13],
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'blog.html', context)

def register_page(request):
    return render(request, 'registration.html')

def login_page(request):
    return render(request, 'login.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/home')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/login_page')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    request.session['user_email'] = user.email
    return redirect('/home')

def logout(request):
    request.session.clear()
    
    return redirect('/')

# def password_reset(request):
#     return render(request, 'password_reset.html')

# def password_reset_request(request):
#     if request.method == "GET":
#         return redirect('/password_reset')
    
#     user = User.objects.get(email=request.POST['email'])
#     request.session['user_id'] = user.id
#     request.session['user_email'] = user.email
#     return redirect('/home')

# def password_reset_done(request):
    
#     return render(request, 'password_reset_done.html')  

# def password_change(request):
    
#     return render(request, 'password_change.html')

# def password_reset_done(request):
    
#     return render(request, 'password_reset_done.html')   

# Blog portion of the app.
# render the main news/blog page, wall of posts plus add post functionality

def create_post(request):
    if request.method =='GET':
        return redirect('/home')
    errors = Blogpost.objects.post_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/home')
    else:
        user = User.objects.get(id=request.session["user_id"])
        Blogpost.objects.create(title=request.POST['title'], b_text=request.POST['b_text'], creator=user)
        return redirect('/home')

def delete_post(request, post_id):
    if request.method =='GET':
        return redirect('/home')
    delete_this= Blogpost.objects.get(id=post_id)
    delete_this.delete()
    return redirect('/home')

# like this post
def like_post(request, post_id):
    user = User.objects.get(id=request.session["user_id"])
    post = Blogpost.objects.get(id=post_id)
    user.user_liked_post.add(post)

    return redirect('/home')

# dislike this post
def dislike_post(request, post_id):
    user = User.objects.get(id=request.session["user_id"])
    post = Blogpost.objects.get(id=post_id)
    user.user_liked_post.remove(post)
    return redirect('/home')

# # show post for the user
# def show_post(request, user_id):
#     context = {
#         'this_user': User.objects.get(id=user_id),
#     }
#     return render(request, 'my_account.html', context)

# Account portion of the app.

def my_account(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
    }
    return render(request, 'my_account.html', context)

def update_account(request, user_id):
    update_this_user=User.objects.get(id=user_id)
    errors = User.objects.updateme(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect(f'/my_account/{user_id}')
    else:
        update_this_user.first_name = request.POST['first_name']
        update_this_user.last_name = request.POST['last_name']
        update_this_user.street_address = request.POST['street_address']
        update_this_user.zip_code = request.POST['zip_code']
        update_this_user.email = request.POST['email']
        update_this_user.save()
    return redirect(f'/my_account/{user_id}')

def invite_user(request):

    return render(request, 'invite.html')

def invite_confirmation(request):

    return render(request, 'invitation_sent.html')

def invited(request):
    if request.method == "GET":
        return redirect('/')
    errors = Invited.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/invite')
    else:
        user = User.objects.get(id=request.session["user_id"])
        Invited.objects.create(first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            street_address = request.POST['street_address'],
            zip_code = request.POST['zip_code'],
            email = request.POST['email'],
            invited_by = user)
        return redirect('/invite/sent')

# marketplace
def marketplace(request):
    context = {
        'all_items': Item.objects.all().order_by('created_at')[:13],
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'marketplace.html', context)

def create_item(request):
    if request.method =='GET':
        return redirect('/')
    errors = Item.objects.item_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/marketplace')
    else:
        user = User.objects.get(id=request.session["user_id"])
        Item.objects.create(product_name=request.POST['product_name'],
        item_description=request.POST['item_description'], 
        item_price=request.POST['item_price'], 
        contact_info=request.POST['contact_info'], 
        item_brand=request.POST['item_brand'],
        owner=user)
        return redirect('/marketplace')

# more information about the item
def update_item(request, item_id):
    context = {
        'user' : User.objects.get(id=request.session["user_id"]),
        'item' : Item.objects.get(id=item_id),
    }
    return render(request, 'update_item.html', context)

def item_updated(request, item_id):
    update_this_item=Item.objects.get(id=item_id)
    errors = Item.objects.updateme(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect(f'/marketplace/update_item/{item_id}')
    else:
        update_this_item.product_name = request.POST['product_name']
        update_this_item.item_description = request.POST['item_description']
        update_this_item.item_price = request.POST['item_price']
        update_this_item.contact_info = request.POST['contact_info']
        update_this_item.item_brand = request.POST['item_brand']
        update_this_item.save()
    return redirect(f'/marketplace/update_item/{item_id}')

def delete_item(request, item_id):
    if request.method =='GET':
        return redirect('/')
    delete_this= Item.objects.get(id=item_id)
    delete_this.delete()
    return redirect('/marketplace')

def mark_sold(request, item_id):
    user = User.objects.get(id=request.session["user_id"])
    item = Item.objects.get(id=item_id)
    user.user_sold_item.add(item)

    return redirect('/home')

# more information about the item
def item_info(request, item_id):
    context = {
        'user' : User.objects.get(id=request.session["user_id"]),
        'item' : Item.objects.get(id=item_id),
    }
    return render(request, 'item_info.html', context)


# contact us section
def help(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'help.html', context)

def question_confirmation(request):

    return render(request, 'question_sent.html')

def question_sent(request):
    if request.method == "GET":
        return redirect('/')
    errors = Question.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/help')
    else:
        user = User.objects.get(id=request.session["user_id"])
        Question.objects.create(title = request.POST['title'],
            q_text = request.POST['q_text'],
            creator = user)
        return redirect('/help/post')