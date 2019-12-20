from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *


def index(request):
    return render(request, 'login_registration.html')

def process_register(request):
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    errors = User.objects.basic_validator(request.POST)

    if request.session.get('uid') is not None:
        return redirect('/wishes')

    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')

    new_user= User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw,
        )

    request.session['uid'] = new_user.id
    request.session['first_name'] = new_user.first_name

    return redirect('/wishes')




def process_login(request):
    # first checks if user is logged in 
    if request.session.get('uid') is not None:
        return redirect('/wishes')

    found_user= User.objects.filter(email=request.POST['email'])
    if len(found_user) > 0:
        is_pw_correct = bcrypt.checkpw(request.POST['password'].encode(),
                                found_user.first().password.encode())
        if is_pw_correct is True:
            request.session['uid'] = found_user.first().id
            request.session['first_name'] = found_user.first().first_name
            return redirect('/wishes')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/')
    else:
        messages.error(request,"Invalid credentials")
        return redirect('/')



def wishes(request):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')

    content = {
        'user_wishes': Wish.objects.filter(users_who_wished=request.session['uid'], granted=False),
        'wishes_granted': Wish.objects.filter(granted=True),
        
    }
    return render(request,'wishes.html',content)




def wishes_new(request):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')
    

    return render(request,'wishes_new.html')



def wishes_remove(request,wish_id):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')
    
    wish_to_remove = Wish.objects.filter(id=wish_id)
    if len(wish_to_remove) > 0:
        wish_to_remove.first().delete()

    return redirect('/wishes')




def wishes_edit(request,wish_id):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')

    found_wish = Wish.objects.filter(id=wish_id)
    if len(found_wish) > 0:

        content={
            'found_wish': found_wish[0]
        }
        return render(request,'wishes_edit.html',content)




def process_wishes_edit(request):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')

    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/wishes/edit')

    wish_to_update=Wish.objects.get(id=request.POST['wish_id'])
    wish_to_update.item=request.POST['item']
    wish_to_update.desc=request.POST['desc']
    wish_to_update.save()
    return redirect('/wishes')



def wishes_granted(request,wish_id):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')
    wish_to_grant = Wish.objects.filter(id=wish_id,granted=False)
    if len(wish_to_grant) > 0:
        wish_to_grant[0].granted=True
        wish_to_grant[0].save()
    return redirect('/wishes')

def wishes_like(request,wish_id):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')


    # finds wishes excluding user
    found_wish= Wish.objects.filter(id=wish_id).exclude(users_who_wished=request.session['uid'])
    loggin_user = User.objects.get(id=request.session['uid'])
    if len(found_wish) > 0:
        wish_to_like= found_wish[0]

        if loggin_user in wish_to_like.users_who_liked.all():
            wish_to_like.users_who_liked.remove(loggin_user)
        else:
            wish_to_like.users_who_liked.add(loggin_user)

    return redirect('/wishes')




def process_new_wish(request):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')

    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/wishes/new')

    
    Wish.objects.create(
        item=request.POST['item'],
        desc=request.POST['desc'],
        users_who_wished=User.objects.get(id=request.session['uid'])
    )
    return redirect('/wishes')


def wishes_stats(request):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')
    content={
        'granted_wishes': len(Wish.objects.filter(users_who_wished=request.session['uid'],granted=True)),
        'non_granted_wishes':len(Wish.objects.filter(users_who_wished=request.session['uid'],granted=False))
    }
    return render(request,'wishes_stats.html',content)



def logout(request):
    request.session.clear()
    return redirect('/')