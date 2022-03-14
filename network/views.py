import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like


def index(request):
    if request.user.is_authenticated:
        # print(request.user)
        # # gets self followers
        # print(User.objects.filter(user=request.user))
        # object = User.objects.filter(user=request.user)
        # for o in object:
        #     print(o.username)
        objects = Post.objects.filter(user=request.user)

    # print(User.objects.filter(followers=request.user))
    # users = User.objects.filter(followers=request.user)
    # for u in users:
    #     print(Post.objects.filter(user=u))
    # print(Post.objects.filter(user__in=User.objects.filter(followers=request.user)))
    # "posts": Post.objects.filter(user=request.user)
    # post = Post.objects.get(id=14)
    # post.post = "edited succesfully avuthav ra chala goppodivi avthav"
    # post.save()
    else:
        objects = Post.objects.all()
    paginator = Paginator(objects, 10)  # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": page_obj
    })

# objects = Post.objects.all()
#     paginator = Paginator(objects, 10)  # Show 10 posts per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, "network/index.html", {
#         "posts": page_obj
#     })

# fetch('/posts/14', {
#     method: 'PUT',
#     body: JSON.stringify({
#         post: "change chesina js use chesi",
#         editor: "amara",
#     })
# })


@csrf_exempt
@login_required
def edit(request, post_id):
    # editing a new post must be via POST
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # load the edited post

    data = json.loads(request.body)
    print(data)
    editor = data.get("editor", "")
    postedby = Post.objects.get(pk=post_id).user
    post = data.get("post", "")
    print(post)
    # check if user and editor are the same
    if(editor == postedby.username):
        print("came")
        # implement edited tag feature later
        editp = Post.objects.get(id=post_id)
        editp.post = post
        editp.save()
    else:
        return JsonResponse({"error": "You do not have permission to edit this post"}, status=400)
    return JsonResponse({"message": "post edited succesfuuly."}, status=201)


@csrf_exempt
@login_required
def like(request, post_id):
    # editing a new post must be via POST
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    print(data)
    likedby = data.get("likedby", "")
    likedby = User.objects.get(username=likedby)
    likedpost = Post.objects.get(pk=post_id)

    # check if user and editor are the same
    # print("came")
    # Like.objects.all().delete()
    # post = Post.objects.get(id=post_id)
    # post.likes = 0
    # post.save()
    # implement edited tag feature later
    try:
        print(Like.objects.get(post=likedpost.id, user=likedby.id))
        Like.objects.get(post=likedpost, user=likedby).delete()
        post = Post.objects.get(id=post_id)
        post.likes -= 1
        post.save()
    except:
        print("camehere")
        like = Like(
            post=likedpost,
            user=likedby,
        )
        like.save()
        post = Post.objects.get(id=post_id)
        post.likes += 1
        post.save()

    return JsonResponse({"message": "post liked succesfuuly."}, status=201)


@login_required
def following(request):
    objects = Post.objects.filter(
        user__in=User.objects.filter(followers=request.user))
    likes = Like.objects.filter(user=request.user)
    print(likes)
    likedposts = []
    for like in likes:
        print(like)
        likedposts.append(like.post)
    paginator = Paginator(objects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/allposts.html", {
        "posts": page_obj,
        "likedposts": likedposts
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


@login_required
def post(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            post = Post(user=request.user, post=request.POST["post"])
            # print(Post.objects.all())
            # for post in Post.objects.all():
            #     print(post.id, post.post)
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            message = "please login"
            html = "<html><body>%s</body></html>" % message
            return HttpResponse(html)


def allposts(request):
    objects = Post.objects.all().order_by('-datetime')
    # objects = Post.objects.filter(
    #     user__in=User.objects.filter(followers=request.user))
    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user)
        print(likes)
        likedposts = []
        for like in likes:
            print(like)
            likedposts.append(like.post)
    else:
        likedposts = []
    paginator = Paginator(objects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/allposts.html", {
        "posts": page_obj,
        "likedposts": likedposts
    })


@login_required
def follow(request, userid):

    if request.method == "POST":
        profile = User.objects.get(pk=userid)
        curruser = User.objects.get(pk=request.user.id)
        set = User.objects.filter(followers=curruser)
        usernames = []
        for s in set:
            print(s.username)
            usernames.append(s.username)
        if profile.username in usernames:
            profile.followers.remove(curruser)

        else:
            profile.followers.add(curruser)

        return redirect('profile', userid=userid)


def profile(request, userid):

    profile = User.objects.get(pk=userid)
    # print(profile, User.count_followers(profile), User.count_following(profile))
    curr = User.objects.get(pk=request.user.id)
    # print(ganesh, User.count_followers(ganesh), User.count_following(ganesh))

    # lakshman 1 0
    # profile.followers.add(ganesh) adds ganesh as follower to profile i.e lakshman
    # profile.followers.add(ganesh)
    # print(request.user)
    # print((User.objects.filter(followers=ganesh)))
    set = User.objects.filter(followers=curr)
    usernames = []
    for s in set:
        # print(s.username)
        usernames.append(s.username)
    # print(usernames)
    # print(User.objects.get(username=profile))
    if profile.username in usernames:
        # print("yes")
        follow = "Unfollow"
    else:
        follow = "Follow"
    # print(profile.email)

    followers = User.count_followers(profile)
    following = User.count_following(profile)
    if profile != request.user:
        button = True
    else:
        button = False
    objects = Post.objects.filter(user=profile)
    paginator = Paginator(objects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "profile": profile,
        "followers": followers,
        "following": following,
        "posts": page_obj,
        "button": button,
        "follow": follow
    })
