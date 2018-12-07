from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Reviews.models import Review
from django.core import serializers
from django.utils import timezone


# Create your views here.


def addReviewPage(request):
    context = {}
    return render(request, 'Reviews/addReview.html', context)

def displayReviews(request):
    context = {}
    return render(request, 'Reviews/getReview.html', context)

def getReviews(request, l):
    if request.is_ajax():
        results = Review.objects.filter(location=l)
        data = serializers.serialize("json", results)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

@csrf_exempt
def submitReview(request):
    print("Hello")
    if request.is_ajax() and request.method == 'POST':
        r = Review(author=request.POST['author'],location=request.POST['location'],reviewText=request.POST['review'])
        r.save()
        return HttpResponse("Hello")
    else:
        raise Http404
