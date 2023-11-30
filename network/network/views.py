from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from .models import *
from django.views.decorators.csrf import csrf_exempt



def addPost(request):
    if request.method == "POST":
        
        content = request.POST['postContent']
        user = request.user
        post = Post(user=user,content=content)
        post.save()
        return redirect('index')
    

def follow(request, requestUserID, postUserID):
    
    if request.method == "POST" and requestUserID != postUserID:
        
        requestUser = User.objects.get(pk=requestUserID)
        postUser = User.objects.get(pk=postUserID)
        
        # Check if postUser is not already in the followers of requestUser
        if postUser not in requestUser.following.all():
            requestUser.following.add(postUser)
  
    if requestUserID == postUserID:
        return render(request, "network/error.html", {
            "error": "Error: cannot follow self"
        })    
    
    return redirect('profile', postUserID=postUserID)


def following(request, userID):
    
    user = User.objects.get(pk=userID)
    followingIDs = user.following.values_list('id', flat=True)
    userFollowingPosts = Post.objects.filter(user__id__in=followingIDs).order_by("id").reverse()
    
    return render(request, "network/following.html", {
        "userFollowingPosts": userFollowingPosts
    })


def index(request):
    
    allPosts = Post.objects.all().order_by("id").reverse()
    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "allPosts": page_obj,
        
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def profile(request, postUserID): #clicking on user name will load this poster's profile page, or the user's profile
    # show # of followers, # of people user follows
    postUser = User.objects.get(pk=postUserID)
    postFollowers = postUser.followers.all()
    postFollowing = postUser.following.all()
    postUserPosts = Post.objects.filter(user=postUser).order_by("id").reverse()
    
    followerCount = 0
    followingCount = 0
    for follower in postFollowers:
        followerCount += 1
    for user in postFollowing:
        followingCount += 1
        
    #show user posts in reverse chronological order
    return render(request, "network/profile.html", {
        "postUser": postUser,
        "postFollowers": postFollowers,
        "followerCount": followerCount,
        "postFollowing": postFollowing,
        "followingCount": followingCount,
        "postUser": postUser,
        "requestUser": request.user,
        "postUserPosts": postUserPosts
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
@csrf_exempt
def postJSON(request, postID):
    
    #query for requested user
    try:
        post = Post.objects.get(pk=postID)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    #return post model as JSON
    except post.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    #return user model as JSON
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    #update post likes
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            post.likes = data["likes"]
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({
            "error": "GET or PUT request required"
        }, status=400)
    
    
def unfollow(request, requestUserID, postUserID):
    if request.method == "POST" and requestUserID != postUserID:
         
        requestUser = User.objects.get(pk=requestUserID)
        postUser = User.objects.get(pk=postUserID)
        requestUser.followers.remove(postUser)
        if postUser in requestUser.following.all():
            requestUser.following.remove(postUser)
    
    if requestUserID == postUserID:
        return render(request, "network/error.html", {
            "error": "Error: cannot follow self"
        })    
    
    return redirect('profile', postUserID=postUserID)
