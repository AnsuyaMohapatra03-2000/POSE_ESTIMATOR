import warnings

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponse
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

global isAuthenticate
isAuthenticate = False

# import os

# current_directory = os.getcwd()
# print("Current Directory:", current_directory)


df=pd.read_csv('/home/aconot10/Desktop/real-time-pose-detection/posedetect/webcam/pos.csv')
from sklearn.model_selection import train_test_split


x=df.drop('pose',axis=1)
y=df['pose']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=1)


### SVM Classifier
from sklearn.svm import SVC
dt_clf=SVC(C=25,kernel='linear',random_state=2)
dt_clf.fit(x_train,y_train)
dt_clf.score(x_test,y_test)

# def convert_to_list(a):
#     z=""
#     for i in a:
#         z+=str(i)
#     z=list(map(str,z.split("\n")))
#     z=z[:-1]
#     for i in range(len(z)):
#         z[i]=z[i].split(":")
#         z[i]=float(z[i][1])
#     return z

def convert_landmark_data_to_list(landmark_data):
    # Assuming landmark_data is a list of dictionaries received from the POST request
    landmarks_list = []
    # print(landmark_data['landmarkData'])
    # for landmark in landmark_data:
    #     print(landmark)
    for i in landmark_data['landmarkData']:
        for j in i.values():
            landmarks_list.append(j)
    return landmarks_list
        # # Extract 'x', 'y', 'z' values from each landmark dictionary
        # x = landmark.get('x')
        # y = landmark.get('y')
        # z = landmark.get('z')

        # # Create a new dictionary containing 'x', 'y', 'z' keys and their values
        # landmark_dict = {'x': x, 'y': y, 'z': z}

        # # Append the dictionary to the landmarks_list
        # landmarks_list.append(landmark_dict)

    return landmarks_list

def classifyPose(image_landmarks):
    label = 'Unknown Pose'
    coordinates = np.array(image_landmarks)
    coordinates = coordinates.reshape(1, -1)
    label = str(dt_clf.predict(coordinates)[0])
    return label

@login_required(login_url='login')


def home(request):
    return HttpResponse("Hello World")

def register(request):
    return render(request,'register.html')

def HomePage(request):
    global isAuthenticate
    if isAuthenticate == True:
     return render (request,'camera.html')
    
    else:
     return redirect('login')

def AboutPage(request):
    global isAuthenticate
    if isAuthenticate == True:
     return render (request,'about.html')
    
    else:
     return redirect('login')

def ImagePage(request):
    global isAuthenticate
    if isAuthenticate == True:
     return render (request,'image.html')
    
    else:
     return redirect('login')




def process_coordinates(request):
    print("This is the process coordinate view !!")

def SignupPage(request):
    
    

    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            try:
                user = User.objects.get(username=uname)
                return HttpResponse("Username already exists!!")  # Username exists
            except User.DoesNotExist:
                my_user=User.objects.create_user(uname,email,pass1)
                my_user.save()
                return redirect('login')



    return render (request,'signup.html')

def LoginPage(request):
    global isAuthenticate
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            isAuthenticate = True
            login(request,user)
            return redirect('about')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    global isAuthenticate
    isAuthenticate = False
    logout(request)
    return redirect('login')
    

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Use only for simplicity, consider using proper CSRF protection in production
def receive_landmark_data(request):
    print("Inside the receive landmark data")
    if request.method == 'POST':
        # Parse JSON data from the request
        data = json.loads(request.body)

        detected_pose=classifyPose(convert_landmark_data_to_list(data))
        # Process the received data
        # TODO: Add your logic to handle the landmark data

        # Return a JSON response
        return JsonResponse({'status': 'success','pose':detected_pose})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
