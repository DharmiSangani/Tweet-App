from django.shortcuts import render
from .models import Tweet
from .forms import Tweetform, UserRegistrationFrom, SerchForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout


# Create your views here.

def index(request):
    return render(request, "index.html")

def tweet_list(request):
    tweets=Tweet.objects.all().order_by('created_at')
    return render(request, 'tweet_list.html',{'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method=="POST":
      form=Tweetform(request.POST, request.FILES)
      if form.is_valid():
        tweet=form.save(commit=False) 
        tweet.user = request.user
        tweet.save()
        return redirect('tweet_list')
    else:
      form=Tweetform()
    return render(request,'tweet_form.html', {'form':form})

@login_required
def tweet_edit(request, tweet_id):
   tweet=get_object_or_404(Tweet, pk=tweet_id, user=request.user)
   if request.method=="POST":
    form=Tweetform(request.POST, request.FILES, instance=tweet)
    if form.is_valid():
       tweet=form.save(commit=False)
       tweet.user=request.user
       tweet.save()
       return redirect("tweet_list")
   else:
      form=Tweetform(instance=tweet)
   return render(request,'tweet_form.html', {'form':form})

@login_required
def tweet_delete(request, tweet_id):
    tweet=get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method=='POST':
       tweet.delete()
       return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html', {'tweet':tweet})
 

def register(request):
   if request.method=="POST":
      form=UserRegistrationFrom(request.POST)
      if form.is_valid():
         user=form.save(commit=False)
         user.set_password(form.cleaned_data['password1'])
         user.save()
         login(request, user)
         return redirect('tweet_list')
   else:
      form=UserRegistrationFrom()
   return render(request,'registration/register.html', {'form':form})

def search(request):
   if request.method=="POST":
    form = SerchForm(request='POST')
    if form.is_valid():
            query = form.cleaned_data['query']
            results = Tweet.objects.filter(content__icontains=query)  # Adjust the filter to match your model fields
    return render(request, 'search.html', {'form': form, 'results': results})

def logout_view(request):
    logout(request)
    return redirect('login') 