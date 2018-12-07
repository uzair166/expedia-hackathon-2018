from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Reviews.models import Review

# Create your views here.

def index(request, question_id):
    return HttpResponse("You're looking at index %s" % question_id)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def addReviewPage(request):
    context = {}
    return render(request, 'Reviews/addReview.html', context)

@csrf_exempt
def submitReview(request):
    print("Hello")
    if request.is_ajax() and request.method == 'POST':
        r = Review(author=request.POST['author'],location=request.POST['location'],reviewText=request.POST['review'])
        r.save()
        return HttpResponse("Hello")
    else:
        raise Http404
