from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .models import Question

def index(request):
    # Get the 5 last questions
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context  = {
        'latest_question_list' : latest_question_list
    }
    return render(request=request, template_name='polls/index.html',context=context)

def detail(request, question_id):
    return HttpResponse("Youre looking at question %s." % question_id)

def results(request, question_id):
    response = "You are looking at the results of question {}"
    return HttpResponse(response.format(question_id))

def vote(request, question_id):
    return HttpResponse("You are voting on question {}".format(question_id))


