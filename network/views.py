import datetime, json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Post, User



def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "network/index.html", {
            "posts": sorted(Post.objects.all(), key=lambda x: x.timestamp, reverse=True)
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


# Receival of like change from Fetch API
def likechange(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        u = data["username"]
        p = Post.objects.all().get(id = data["postID"])
        print("\n-----------------------------------------------------\n\n--- (1.1) The like change is received from fetch API...\n--- (1.2) ...processed in views.py...\n--- (1.3) ...then sent back to same user who sent it\n\n-----------------------------------------------------")

        if Post.objects.all().get(id = data["postID"]).likes.filter(username=data["username"]).exists():
            # There was already a like from the user for that post so the change is a dislike
            p.likes.remove(User.objects.get(username=u))
            # Fetch API response to the client to inform about the dislike success
            return JsonResponse({"message": "\n\nServer successfully processed the DISLIKE received from the fetch API \n\n"}, status=200)

        else:
            # There was already a like from the user for that post so the change is a like
            p.likes.add(User.objects.all().get(username=u))
            # Fetch API response to the client to inform about the like success
            return JsonResponse({"message": "\n\nServer successfully processed the LIKE received from the fetch API \n\n"}, status=200)


# New post is submitted:
def post(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        u = data["username"]
        user = User.objects.all().get(username=u)
        print(user)
        p = Post(user = user, text = data["text"], timestamp = datetime.datetime.now().timestamp())
        p.save()
        print(p)
        # Fetch API response to the client to inform about the Post success
        return JsonResponse({"message": "\n\nServer successfully processed the POST received from the fetch API \n\n"}, status=200)

# Do something about new post data
timestamp = datetime.datetime.now().timestamp()