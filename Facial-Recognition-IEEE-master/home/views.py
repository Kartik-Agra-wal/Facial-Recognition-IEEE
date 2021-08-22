from facial_recog.settings import MEDIA_ROOT
import random
import time
import os
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http.response import StreamingHttpResponse
from django.shortcuts import redirect, render
from django.views.decorators import gzip

from home.camera import VideoCamera

from .forms import *


def Index(request):
    return render(request, 'home/index.html')


@gzip.gzip_page
def webcam_feed(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

def gen(camera):
    while True:
        frame, _ = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(1/30)

def register(request):
	if request.method == "POST":
		f = NewUserForm(request.POST)
		if f.is_valid():
			user=f.save()
			messages.success(request, "Account created successfully")
			login(request, user)
			return redirect("register_face")
	else:
		f = NewUserForm()
		
	return render(request, "home/signup.html", {"form": f})

def signup_gen(camera, user):
	count = 0
	folder = os.path.join(MEDIA_ROOT,user.username)
	os.makedirs(folder, exist_ok=True)
	while True:
		if count == 50:
			return None
		
		frame, faces = camera.get_frame()
		if len(faces) > 0:
			file_id=random.randint(1,100)
			with open(os.path.join(folder, f"{file_id}.jpg"), 'wb') as f:
				f.write(frame)
			count += 1
		yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		time.sleep(1/30)

@gzip.gzip_page
def signup_facecapture(request):
    cam = VideoCamera()
    return StreamingHttpResponse(signup_gen(cam, request.user), content_type="multipart/x-mixed-replace;boundary=frame")
    
def register_face(request):
	return render(request, "home/signup_facecapture.html")
