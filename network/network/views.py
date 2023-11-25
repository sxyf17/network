from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
import json
from django.core.paginator import Paginator


from .models import *


def addPost(request):
    if request.method == "POST":
        
        content = request.POST['postContent']
        user = request.user
        post = Post(user=user,content=content)
        post.save()
        return redirect('index')

def follow(request, requestUserID, postUserID):
    
    if request.method == "POST" and requestUserID is not postUserID:
         
        requestUser = User.objects.get(pk=requestUserID)
        postUser = User.objects.get(pk=postUserID)
        postUser.followers.add(requestUser)
    
    if requestUserID == postUserID:
        return render(request, "network/error.html", {
            "error": "Error: cannot follow self"
        })    
    
    return redirect('profile', userID=postUserID)


def index(request):
    
    allPosts = Post.objects.all().order_by("id").reverse()
    p = Paginator(allPosts, 10)
    
    return render(request, "network/index.html", {
        "allPosts": allPosts,
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


def userJSON(request, userID):
    
    #query for requested user
    try:
        user = User.objects.get(pk=userID)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    #return user model as JSON
    if request.method == "GET":
        return JsonResponse(user.serialize())
    
    #update user followers/following
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("followers") is not None:
            user.followers = data["followers"]
        if data.get("following") is not None:
            user.following = data["following"]
        user.save()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({
            "error": "GET or PUT request required"
        }, status=400)


def profile(request, userID): #clicking on user name will load this poster's profile page, or the user's profile
    # show # of followers, # of people user follows
    postUser = User.objects.get(pk=userID)
    postFollowers = postUser.followers.all()
    postFollowing = postUser.following.all()
    userPosts = Post.objects.filter(user=postUser).order_by("id").reverse()
    
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
        "userPosts": userPosts
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
    
    
def unfollow(request, requestUserID, postUserID):
    if request.method == "POST" and requestUserID is not postUserID:
         
        requestUser = User.objects.get(pk=requestUserID)
        postUser = User.objects.get(pk=postUserID)
        requestUser.followers.remove(postUser)
    
    if requestUserID == postUserID:
        return render(request, "network/error.html", {
            "error": "Error: cannot follow self"
        })    
    
    return redirect('profile', userID=postUserID)
