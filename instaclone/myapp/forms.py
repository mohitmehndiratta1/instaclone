from django import forms
from models import UserModel
from models import PostModel, PostLikeModel, PostCommentModel

class SignUpForm(forms.ModelForm):
  class Meta:
    model = UserModel
    fields=['email','username','name','password']

class LoginForm(forms.ModelForm):
  class Meta:
    model = UserModel
    fields = ['username', 'password']

class PostForm(forms.ModelForm):
  class Meta:
    model = PostModel
    fields = ['image', 'caption']

class LikeForm(forms.ModelForm):
  class Meta:
    model = PostLikeModel
    fields = ['post']

class CommentForm(forms.ModelForm):
  class Meta:
    model = PostCommentModel
    fields = ['comment_text','post']