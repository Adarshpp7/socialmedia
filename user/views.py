import json
from django.contrib.auth.models import User, update_last_login
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.generic import View,TemplateView,ListView
from django.views.generic.edit import CreateView
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import UserRegisterForm,AuthenticationForm
import base64
from django.core.files.base import ContentFile
from django.contrib import messages
from django.db.models import Q
import uuid
from .models import Followings, User_Profile,Post,Like,Comments,Followers, Users_Room, Messages

# Create your views here.

@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    
        model = Post
        template_name = 'default.html'
        context_object_name = 'posts'
        ordering = ['-date_posted']
        paginate_by = 10

        def get_context_data(self, **kwargs):
            context = super(HomeView, self).get_context_data(**kwargs)
            if self.request.user.is_authenticated:
                followers = Followings.objects.filter(to_user=self.request.user)
                print(followers,'hellpppp')
                context['followers'] = followers
            return context
         
class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'register.html'
  success_url = reverse_lazy('LoginView')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully"


class LoginView(View):
    
    def get(self,request):
        if self.request.session.has_key('userkey'):
            return redirect('HomeView')
        else:
            return render(request, 'login.html',{'form':AuthenticationForm})
    
    def post(self,request):
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data.get('username'), password = form.cleaned_data.get('password'))
            if user is None:
                return render(request, 'login.html', {'form':form, 'invalid_creds':True})
            else:
                form.confirm_login_allowed(user)
                login(request,user)
                self.request.session['userkey'] = 'user'
                print(self.request.session['userkey'])
                return redirect('HomeView')
      
        else:
            messages.info(request,'sorry, that login was invalid. Please try again.')
            return redirect('/')
     
            
            
@method_decorator(login_required, name='dispatch')    
class SettingsView(TemplateView):
    template_name = 'default-settings.html' 


@method_decorator(csrf_exempt, name='dispatch')
class PasswordChangeView(View):
    def get(self, request):
        return render(request, 'password.html')
    def post(self, request):
        check_status = check_password(request.POST['password'],request.user.password)
        if check_status == True:
            print('hellooooooooo')
            request.user.set_password(request.POST['password1'])
            request.user.save()
            return JsonResponse('true', safe=False)
        else:
            print('heyyyyyyyyyyyyyyyyyy')
            return JsonResponse('false', safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class DetailsChangeView(View):
    def get(self, request):
        return render(request, 'editdetails.html')
    def post(self, request):
        current_user = User_Profile.objects.get(id=request.user.id)
        if request.POST['first_name'] == '' or request.POST['last_name'] == '' or request.POST['email'] == '' or request.POST['phone'] == '' or request.POST['country'] == '' or request.POST['city'] == '' or request.POST['gender'] == '' :
            messages.info(request,'add every details properly')
            return redirect('DetailsChangeView')
      
        else:  
            # image1 = request.FILES.get('image2')
            image1 = request.POST['imageurl1']
            print(image1,'yesssssssss')
            # if image1==None:
                # messages.info(request,'crop every image properly')
                # return redirect(DetailsChangeView)
            # else:
                # format, imgstr = image1.split(';base64,')
                # ext = format.split('/')[-1]
                # img1 = ContentFile(base64.b64decode(imgstr),name= request.user.username+ '.' + ext)

            current_user.first_name = request.POST['first_name']
            current_user.last_name = request.POST['last_name']
            current_user.email = request.POST['email']
            current_user.phone_number = request.POST['phone']
            current_user.country = request.POST['country']
            current_user.location = request.POST['city']
            current_user.gender = request.POST['gender']
            # current_user.birth_date = request.POST['dateObirth']
            if image1 != '':
                format, imgstr = image1.split(';base64,')
                ext = format.split('/')[-1]
                img1 = ContentFile(base64.b64decode(imgstr),name= request.user.username+ '.' + ext)
                current_user.image = img1
            current_user.save()
            
            return redirect('HomeView')

@login_required
def user_profile_view(request, id):
   
    selected_user = User_Profile.objects.get(id=id)
    posts = Post.objects.filter(user=selected_user)
    post_count = posts.count()
    friends_count = selected_user.friends.count()
    followers_count = Followings.objects.filter(to_user=selected_user).count() + friends_count
    following_count = Followings.objects.filter(from_user=selected_user).count() + friends_count
    if selected_user in request.user.friends.all():
        relation_stat = 'Unfriend'
    elif Followings.objects.filter(from_user=request.user, to_user= selected_user).exists():
        relation_stat = 'Unfollow'
    elif Followings.objects.filter(from_user=selected_user, to_user=request.user).exists():
        relation_stat = 'Followback'
    else:
        relation_stat = 'Follow'
    context = {'this_user':selected_user, 'posts':posts , 'post_count':post_count,'friends_count':friends_count, 'followers_count':followers_count, 'following_count':following_count, 'relation_stat':relation_stat}
    return render(request,'user-page.html',context)

@login_required
def users_list(request):
    # users = User_Profile.objects.exclude(id=request.user.id)
    follow = Followers.objects.filter(Q(to_user=request.user) | Q(from_user=request.user))
    id_list = [request.user.id,11]
    for follow in follow:
        if follow.from_user == request.user:
            id_list.append(follow.to_user.id)
        elif follow.to_user == request.user:
            id_list.append(follow.from_user.id)

    user1 = User_Profile.objects.exclude(id__in =id_list) 
    # print(follow)


    context = {
        'users': user1,
    }
    return render(request, "users_list.html", context)

@method_decorator(login_required, name='dispatch')
class CreatePostView(View):
    
    def get(self, request):
        return render(request, 'createpost.html')

    def post(self, request):
        # image = request.FILES.get('image1')
        image = request.POST['imageurl1']
        description = request.POST['description']
        if image == '' and description == '':
            messages.info(request,'no data entered')
            return redirect('CreatePostView')
        else:
            if image != '':
                format, imgstr = image.split(';base64,')
                ext = format.split('/')[-1]
                img1 = ContentFile(base64.b64decode(imgstr),name= request.user.username+ '.' + ext)
                Post.objects.create(description = description, pic = img1, user = request.user)
            else:
                Post.objects.create(description = description, user = request.user)
        
       
        # messages.success(request, f'Posted Successfully')
        return redirect('HomeView')
    
@login_required
def like(request,id):
    post = Post.objects.get(id = id)
    liked = False
    like = Like.objects.filter(user = request.user , post = post)
    if like:
        like.delete()
        post.likes_count -= 1
        print(post.likes_count)
        post.save()
    else:
        Like.objects.create(user = request.user , post = post)
        post.likes_count += 1
        print(post.likes_count)
        post.save()
        liked = True
    return JsonResponse(liked, safe=False)


@method_decorator(login_required, name='dispatch')
class CommentPostView(View):

    def get(self, request,id):
        post = Post.objects.get(id=id)
        comments = Comments.objects.filter(post=post)
        return render(request, 'comments.html', {'comments': comments, 'post': post})
    
    def post(self, request, id):
        post = Post.objects.get(id=id)
        comment = request.POST['comment']
        Comments.objects.create(post=post,comment=comment,user=request.user)
        post.comments_count += 1
        post.save()
        return JsonResponse('true', safe=False)

@login_required
def follow(request,id):
    to_user = User_Profile.objects.get(id=id)
    if request.GET['content'] =='Follow':
        Followings.objects.create(to_user=to_user,from_user=request.user)
        Followers.objects.create(from_user=request.user,to_user=to_user)
    elif request.GET['content'] == 'Unfollow':
        Followings.objects.filter(to_user=to_user,from_user=request.user).delete()
        Followers.objects.filter(to_user=to_user, from_user = request.user).delete()
        # to_user.followers.remove(request.user)
        # request.user.followings.remove(to_user)
    return JsonResponse('true', safe=False)

@login_required
def followback(request,id):
    user = User_Profile.objects.get(id=id)
    Followings.objects.filter(from_user=user, to_user=request.user).delete()
    request.user.friends.add(user)
    Followers.objects.create(from_user=request.user, to_user=user)
    return JsonResponse('true', safe=False)
@login_required   
def delete_request(request, id):
    user = User_Profile.objects.get(id=id)
    Followings.objects.filter(from_user=user,to_user=request.user).delete()
    Followers.objects.filter(to_user=request.user,from_user=user).delete()
    return JsonResponse('true', safe=False)
@login_required
def unfriend(request,id):
    user = User_Profile.objects.get(id=id)
    Followings.objects.create(from_user=user, to_user=request.user)
    request.user.friends.remove(user)
    Followers.objects.filter(from_user=request.user, to_user=user).delete()
    return JsonResponse('true', safe=False)

@login_required
def friendslist(request,id):
        friends = request.user.friends.all()
        if id == 1:
            context = {'list': friends , 'category': 'Friends'}
        elif id == 2:
            followers = Followings.objects.filter(to_user=request.user)
            # followers = Followers.objects.filter(to_user=request.user)
            context = {'list': followers ,'list1': friends, 'category': 'Followers'}
        elif id == 3:
            followings = Followings.objects.filter(from_user=request.user)
            context = {'list': followings ,'list1': friends, 'category': 'Following'}
        else:
            return render(request, 'chat_users.html',{'friends':friends} )
        return render(request, 'followlist.html' , context)
@login_required
def start_chat(request,id):
    opted_user = User_Profile.objects.get(id=id)
    if Users_Room.objects.filter(user1=opted_user, user2=request.user).exists():
        user_room = Users_Room.objects.get(user1=opted_user,user2=request.user)
    elif Users_Room.objects.filter(user1=request.user,user2=opted_user).exists():
        user_room = Users_Room.objects.get(user1=request.user, user2=opted_user) 
    else:
        room_name = uuid.uuid1()
        user_room = Users_Room.objects.create(user1=opted_user,user2=request.user,room_name=room_name)
    messages = Messages.objects.filter(users_room=user_room).order_by('date')
    context = {'user':request.user,'receiver':opted_user,'messages':messages,'room_name': user_room.room_name}
    return render(request,'chat.html', context)
@login_required
def search_function(request):
    search_input = request.GET['search_text']  
        # search_result = User_Profile.objects.filter(username__icontains=search_input) or User_Profile.objects.filter(first_name__icontains=search_input) or User_Profile.objects.filter(last_name__icontains=search_input)
        # print(type(search_result))
    if User_Profile.objects.filter(Q(username__icontains=search_input) | Q(first_name__icontains=search_input) | Q(last_name__icontains=search_input)).exists():
        search_result = User_Profile.objects.filter(Q(username__icontains=search_input) | Q(first_name__icontains=search_input) | Q(last_name__icontains=search_input))
        friends_list =[]
        followers_list =[]
        following_list =[]
        not_related =[]
        for i in search_result:
            if i in request.user.friends.all():
                friends_list.append(i)
            elif Followings.objects.filter(from_user=i, to_user=request.user).exists():
                followers_list.append(i)
            elif Followings.objects.filter(from_user=request.user, to_user=i).exists():
                following_list.append(i)
            else:
                not_related.append(i)
        context= {'friends':friends_list,'followers':followers_list,'following':following_list,'not_related':not_related,'search_status':'success'}
        return render(request, 'search.html' , context)
    else:
        context= {'search_status':'failed'}
        return render(request, 'search.html' , context)
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        # return HttpResponseRedirect(settings.LOGIN_URL)
        return redirect('LoginView')
