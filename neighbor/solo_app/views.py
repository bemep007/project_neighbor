from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import Invited, User, Blogpost, Item



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
        return redirect('/blog')
    errors = Blogpost.objects.post_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/blog')
    else:
        user = User.objects.get(id=request.session["user_id"])
        Blogpost.objects.create(author=request.POST['author'], b_text=request.POST['b_text'], creator=user)
        return redirect('/blog')

def delete_post(request, quote_id):
    if request.method =='GET':
        return redirect('/blog')
    delete_this= Blogpost.objects.get(id=quote_id)
    delete_this.delete()
    return redirect('/blog')

# like this post
def like_post(request, post_id):
    user = User.objects.get(id=request.session["user_id"])
    quote = Blogpost.objects.get(id=post_id)
    user.user_liked_post.add(quote)

    return redirect('/blog')

# dislike this post
def dislike_post(request, post_id):
    user = User.objects.get(id=request.session["user_id"])
    post = Blogpost.objects.get(id=post_id)
    user.user_liked_post.remove(post)
    return redirect('/blog')

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
        Invited.objects.invited_user(request.POST)
        return redirect('/invite/sent')

# marketplace
def marketplace(request):
    context = {
        'all_items': Item.objects.all().order_by('created_at')[:13],
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'marketplace.html', context)

# marketplace
def help(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'help.html', context)