from distutils.log import log
from re import sub
from turtle import pos
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Likepost, Profile,Post,Followers
from itertools import chain
import random

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    
    user_following_list=[]
    post_feed=[]
    
    user_following = Followers.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        post_feed_lists=Post.objects.filter(user=usernames)
        post_feed.append(post_feed_lists)
        
    post_feed_list=list(chain(*post_feed))   
    
    all_users=User.objects.all()
    user_following_all=[] 
    
    for user in user_following:
        username_list=User.objects.get(username=user.user)
        user_following_all.append(username_list)
        
    logined_user=User.objects.filter(username=request.user.username)
    suggestion_list=[x for x in list(all_users) if (x not in list(user_following_all) and x not in list(logined_user))]
    random.shuffle(suggestion_list)
    
    username_profile=[]
    username_profile_list=[]
    
    for users in suggestion_list:
        username_profile.append(users.id)
        
    for ids in username_profile:
        profile_object=Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_object)
        
    final_profile_list=list(chain(*username_profile_list))
    
    return render(request,'index.html',{'user_profile': user_profile,'posts':post_feed_list,'final_profile_list':final_profile_list[:5]})

@login_required(login_url='signin')
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    
    if request.method=='POST':
        username=request.POST['username']
        username_object=User.objects.filter(username__icontains=username)
        
        username_profile=[]
        username_profile_list=[]
        
        for users in username_object:
            username_profile.append(users.id)
            
        for ids in username_profile:
            profile_list=Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_list)
            
        username_profile_lists=list(chain(*username_profile_list))
    
    return render(request,'search.html',{'user_profile':user_profile,'username':username,'username_profile_lists':username_profile_lists})

def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        
        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exists')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already in use')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                user_login=auth.authenticate(username=username, password=password)
                auth.login(request,user_login)
                
                user_model=User.objects.get(username=username)
                new_Profile=Profile.objects.create(user=user_model, id_user=user_model.id)
                new_Profile.save()
                return redirect('settings')
        else:
            messages.info(request,'Password did not match. Please try again')
            return redirect('signup')
    else:
      return render(request,'signup.html')
  
@login_required(login_url='signin')
def upload(request):
    user_profile=Profile.objects.get(user=request.user)
    if request.method=='POST':
        user=request.user.username
        user_profileimage=user_profile.profileimage
        image=request.FILES.get('post_image')
        caption=request.POST['caption']
        
        new_post=Post.objects.create(user=user,user_profileimage=user_profileimage,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    
@login_required(login_url='signin')
def like_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    
    post=Post.objects.get(id=post_id)
    
    like_filter=Likepost.objects.filter(username=username,post_id=post_id).first()
    
    if like_filter==None:
        new_like=Likepost.objects.create(username=username,post_id=post_id)
        new_like.save()
        post.likes=post.likes+1
        post.save()
        return redirect('/')
    
    else:
        like_filter.delete()
        post.likes=post.likes-1
        post.save()
        return redirect('/')
    
@login_required(login_url='signin')
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=pk)
    user_no_of_posts=len(user_posts)
    follower=request.user.username
    user=pk
    if Followers.objects.filter(follower=follower,user=user).first():
        submit_button='Unfollow'
    else:
        submit_button='Follow'
    user_followers=len(Followers.objects.filter(user=pk))
    user_following=len(Followers.objects.filter(follower=pk))
    return render (request,'profile.html',{'user_object':user_object,'user_profile':user_profile,'user_posts':user_posts,'user_no_of_posts':user_no_of_posts,'submit_button':submit_button,'user_followers':user_followers,'user_following':user_following})
@login_required(login_url='signin')
def follow(request):
    if request.method=='POST':
        user=request.POST['user']
        follower=request.POST['follower']
        
        if Followers.objects.filter(user=user,follower=follower).first():
            Unfollow_object=Followers.objects.get(user=user,follower=follower)
            Unfollow_object.delete()
            return redirect('/profile/'+user)
        else:
            Follow_object=Followers.objects.create(user=user,follower=follower)
            Follow_object.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')


@login_required(login_url='signin')
def settings(request):
    user_profile=Profile.objects.get(user = request.user)
    
    if request.method=='POST':
        if request.FILES.get('profileimage')==None:
            profileimage=user_profile.profileimage
            bio=request.POST['bio']
            location=request.POST['location']
            Workplace=request.POST['workplace']
            Relationship_status=request.POST['relationship']
        
            
            user_profile.profileimage=profileimage
            user_profile.bio=bio
            user_profile.location=location
            user_profile.Workplace=Workplace
            user_profile.Relationship_status=Relationship_status
            user_profile.save()
        
        if request.FILES.get('profileimage')!=None:
            profileimage=request.FILES.get('profileimage')
            bio=request.POST['bio']
            location=request.POST['location']
            Workplace=request.POST['workplace']
            Relationship_status=request.POST['relationship']
            
        
            
            user_profile.profileimage=profileimage
            user_profile.bio=bio
            user_profile.location=location
            user_profile.Workplace=Workplace
            user_profile.Relationship_status=Relationship_status
            user_profile.save()
        return redirect('settings')
    
    
    return render(request,'setting.html',{'user_profile':user_profile})  
  
  
def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        
        user=auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect(signin)
    else:
       return render(request,'signin.html')
   
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')