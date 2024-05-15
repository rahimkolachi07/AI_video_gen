# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.exceptions import AuthenticationFailed
# from .serializers import UserSerializer
# from .models import User
# import jwt, datetime
# import requests
# from aistory.aws import separate_arrays
# from .models import Prompts
# # AI Story Generation Imports
# from .main import main_story


# Experiment
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Prompts
from django.views.generic import TemplateView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django import forms
import boto3
from .main import main_story
from aistory.aws import separate_arrays
from .utils import generate_string

import re



from random import seed
from random import random
seed(1)

def mode1(request):
    return render(request,'index.html')
def mode2(request):
    return render(request,'about.html')

# Experiment
class HomePage(View):
    def get(self, request):
        return render(request, 'home.html')


class MultipleImageUploadForm(forms.Form):
    images = forms.FileField(widget = forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "accept": "image/*",
            "multiple": "True",
            'blank': "True"
        }), required=False)
    
    input_field = forms.CharField(label='Input Field')
    select_field = forms.ChoiceField(label='Select Field', choices=[('English (US)', 'English (US) en-US')])

@method_decorator(login_required(login_url='login'), name='dispatch')
class Prompt(View):
    def get(self, request):
        form = MultipleImageUploadForm()
        user_prompts = Prompts.objects.filter(user_id=request.user)
        print(user_prompts)
        if(len(user_prompts) == 0):
            user_name_id =  None   
            return render(request, 'prompt.html', {'form': form , "user_name_id" : user_name_id})   
        else: 
            user_video_url = user_prompts[0].url
            user_name_id = self.extract_folder_name(user_video_url)
            return render(request, 'prompt.html', {'form': form , "user_name_id" : user_name_id})


    def extract_folder_name(self, url):
        # Regular expression to extract the text between '.com/' and '/image'
        pattern = r'.com/([^/]+)/video'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return None
    
    def post(self, request):
        files = request.FILES.getlist('images')
        input_field_value = request.POST.get('input_field')
        select_field_value = request.POST.get('select_field')
        username = ""
        user = {}
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            user = request.user
            # Prompts.objects.create(user_id, video_url)
        
        promptId = generate_string(13)
        print(promptId)
        for file in files:
            self.upload_file_to_s3(file, promptId , username)
        print(username+""+promptId)
        folder_name = username+""+promptId
        
        urls =  main_story(title=input_field_value, lang=select_field_value, loc=folder_name, pic=len(files) > 0)
        [image_files, video_files, audio_files, csv_files]=separate_arrays(urls_dict=urls)

        prompt = Prompts(user=user, url=video_files[0])
        prompt.save()
        
        return redirect('prompt')  # Redirect to success page after successful upload


    def upload_file_to_s3(self,file, prompt_id , username):
        s3 = boto3.client('s3', aws_access_key_id='AKIAXYKJRRBQSNB7NKG7', aws_secret_access_key='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')
        bucket_name = 'story21'
        folder_name = username+""+prompt_id
        folder_path = f'{folder_name}/raw_images/'  # Adjust the folder structure as needed
        # Create the nested folders
        s3.put_object(Bucket=bucket_name, Key=(folder_path))
        # Upload the file to the specified folder
        s3.upload_fileobj(file, bucket_name, f'{folder_path}{file}')
    
# prompt End


class SignupPage(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        print(uname)
        print(pass1)
        print(pass2)

        # Check if any field is empty
        if not (uname and email and pass1 and pass2):
            error_message = 'Please fill out all fields'
            return render(request, 'signup.html', {'error_message': error_message})

        # Check if passwords match
        if pass1 != pass2:
            error_message = 'Passwords do not match'
            return render(request, 'signup.html', {'error_message': error_message})

        # Check if username already exists
        if User.objects.filter(username=uname).exists():
            error_message = 'Username already exists'
            return render(request, 'login.html', {'error_message': error_message})

        # If all checks pass, create the user
        user = User.objects.create_user(username=uname, email=email, password=pass1)
        user.save()
        return redirect('login')

class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('prompt')
        else:
            error_message = "Username or Password is incorrect!!!"
            return render(request, 'login.html', {'error_message': error_message})

class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    

class Success(View):
    def get(self, request):
        return render(request, 'success.html')
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class Userstories(View):
    def get(self, request):
        if request.user.is_authenticated:
            # prompt = Prompts(user=request.user, url="http://localhost:8000/api/prompt")
            # prompt.save()
            user_prompts = Prompts.objects.filter(user_id=request.user)
            if(len(user_prompts) == 0):
                return render(request , 'NotGenerated.html')
        return render(request, 'user_prompts.html' , {
            'user_prompts': user_prompts
        })



# End of experiment



# # Create your views here.
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user = User.objects.filter(email=email).first()

#         if user is None:
#             raise AuthenticationFailed('User not found!')

#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password!')

#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()
#         }

#         token = jwt.encode(payload, 'secret', algorithm='HS256')

#         response = Response()

#         response.set_cookie(key='jwt', value=token, httponly=True)
#         response.data = {
#             'jwt': token,
#             'name' : user.name
#         }
#         return response


# class UserView(APIView):

#     def get(self, request):
#         token = request.COOKIES.get('jwt')
#         print(token)
#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')

#         user = User.objects.filter(id=payload['id']).first()
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


# class LogoutView(APIView):
#     def post(self, request):
#         response = Response()
#         response.delete_cookie('jwt')
#         response.data = {
#             'message': 'success'
#         }
#         return response
    

# # title,lang,loc,pic
# class Prompt(APIView):
#     def post(self, request):
#         try:
#             response = Response()
#             title = request.data['title']
#             lang = request.data['lang']
#             loc = request.data['loc']
#             pic = request.data['pic']
#             user = request.data['user']
#             print(loc)
            
#             urls =  main_story(title=title, lang=lang, loc=loc, pic=pic)
#             [image_files, video_files, audio_files, csv_files]=separate_arrays(urls_dict=urls)
#             response.data = {
#                 "title" : request.data['title'],
#                 "id" : str(random()),
#                 "images":image_files,
#                 "video" : video_files,
#                 "audio" : audio_files,
#                 "doc" : csv_files
#             }
#             user = User.objects.filter(user=user).first()
#             prompt = Prompts.objects.create(user , video_files[0])
#             return response
#         except requests.exceptions.RequestException as e:
#             raise SystemExit(e)
        
# class Sotries(APIView):
#     def get(self,request):
#         response = Response()
#         user = request.data['user']
#         userprompts = Prompts.objects.filter(name=request.data['name'])
#         response.data = {
#             "userprompts" : userprompts
#         }
#         return response