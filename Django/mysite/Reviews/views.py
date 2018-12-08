from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Reviews.models import Review
from django.core import serializers
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import time
import ffmpy
import json
import time
import os
import os.path


# Create your views here.


def addReviewPage(request):
    context = {}
    return render(request, 'Reviews/addReview.html', context)

def displayReviews(request):
    context = {}
    return render(request, 'Reviews/getReview.html', context)

def getReviews(request, l):
    if request.is_ajax():
        found = False
        results = Review.objects.filter(location=l).order_by('-upvotes','-datePosted')
        if len(results) == 0:
            wordsInSearch = l.split(" ")
            for word in wordsInSearch:
                results = Review.objects.filter(location=word).order_by('-upvotes','-datePosted')
                if len(results) > 0:
                    found = True
                    break
        else:
            found = True
        if found:
            data = serializers.serialize("json", results)
        else:
            data = {'return':"No Data"}
            data = json.dumps(data)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

@csrf_exempt
def incrementUpvote(request):
    if request.is_ajax() and request.method == 'POST':
        r = Review.objects.get(pk=request.POST['idd'])
        r.upvotes = r.upvotes+1
        r.save()
        return HttpResponse("hello")

@csrf_exempt
def submitReview(request):
    if request.is_ajax() and request.method == 'POST':
        r = Review(author=request.POST['author'],location=request.POST['location'],reviewText=request.POST['review'])#,datePosted=datetime.date.today())
        r.save()
        return HttpResponse("Hello")
    else:
        raise Http404

def getAudio(request):
        if os.path.isfile("Speech.wav"):
            os.remove("Speech.wav")
        if os.path.isfile("Speech.flac"):
            os.remove("Speech.flac")
        duration = 5 # sec
        fs = 48000
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()

        recog = sr.Recognizer()
        scipy.io.wavfile.write("Speech.wav", 48000, recording)
        ff = ffmpy.FFmpeg(inputs={'Speech.wav': None},outputs={'Speech.flac': None})
        ff.run()
        harvard = sr.AudioFile("Speech.flac")
        with harvard as source:
            audio = recog.record(source)
        spokenWords = ""
        try:
            spokenWords = recog.recognize_google(audio).lower()
        except:
            spokenWords = ""
        dict = {'message':spokenWords}
        jsonFile = json.dumps(dict)
        os.remove("Speech.wav")
        os.remove("Speech.flac")
        return HttpResponse(jsonFile, content_type='application/json')
