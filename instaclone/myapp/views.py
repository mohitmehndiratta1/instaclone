from __future__ import unicode_literals

from django.shortcuts import render,redirect
from datetime import datetime
from models import UserModel , SessionToken , PostModel, PostLikeModel, PostCommentModel
from form import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from instaclone.settings import BASE_DIR

from imgurpython import ImgurClient

from django.contrib.auth.hashers import make_password, check_password

YOUR_CLIENT_ID = "a6aafcb28ec79df"
YOUR_CLIENT_SECRET = "d080ec60896f82ded7822335c1e42ecda3170efa"


def signup_view(request):
    today = datetime.now()
    if request.method == "GET":
        form = SignUpForm()

    elif request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html')


    return render(request, 'index.html', {'today':today}, {'form':form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:

                if check_password(password, user.password):
                    token = SessionToken(user = user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response


                else:
                    print 'User is invalid'

    elif request.method == 'GET':
        form = LoginForm()

    return render(request, 'login.html')




def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == "GET":
            form = PostForm()
            return render(request, 'post.html', {'form' : form})

        elif request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                path = str(BASE_DIR +"/" +post.image.url)
                print path
                client = ImgurClient(YOUR_CLIENT_ID, YOUR_CLIENT_SECRET)
                post.image_url = client.upload_from_path(path, anon=True)['link']

                post.save()
                return redirect('/feed/')

    else:
        return redirect('/login/')

def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            posts = PostModel.objects.all().order_by('-created_on')
            for post in posts:

                existing_like = PostLikeModel.objects.filter(post_id=post_id, user=user).first()
                if existing_like:
                    post.has_liked = True

                if not existing_like:
                    PostLikeModel.objects.create(post_id=post_id, user=user)
                else:
                    existing_like.delete()

                return redirect('/feed/')


        else:
            return redirect('/feed/')


    else:
        return redirect('/login/')

def comment_view(request):
  user = check_validation(request)
  if user and request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      post_id = form.cleaned_data.get('post').id
      comment_text = form.cleaned_data.get('comment_text')
      comment = PostCommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
      comment.save()
      return redirect('/feed/')
    else:
      return redirect('/feed/')

  else:
    return redirect('/login')


def check_validation(request):
  if request.COOKIES.get('session_token'):
    session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
    if session:
      return session.user
  else:
    return None