from django.http import HttpResponseRedirect, HttpResponse
#from django.http import Http404
#from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Question, Choice

# Create your views here.
#First Index View
'''def index(request):
    return HttpResponse("Hello, word.  You're at the polls index.")
'''

#second Index View
'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([p.question_text for p in latest_question_list])
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list
    }
    #return HttpResponseoutput
    return HttpResponse(template.render(context, request))
'''

#same as second but with render shortcut
''' last version of index prior to using generic views
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
'''

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

#orig detail
'''
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
'''

#second detail
'''
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
'''

''' last version of detail prior to usign generic views
#updated detail
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #choices = Question.get_choices(question)
    #choices = choices.split(',')
    #return render(request, 'polls/detail.html', {'question': question, 'choices': choices})
    return render(request, 'polls/detail.html', {'question': question})
'''

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

#first version of results
'''
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
'''

'''last version of results prior to using generic views
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
'''

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#first vote view
'''
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
'''


#second vote view
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
        '''Request.POST is a dictionary-like object that lets you access submitted data by key name.
           In this case, request.POST['choice'] returns the ID of the selected choice, as a string.
           request.POST values are always strings.'''
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data.  This prevents data from being posted twice if a
        # user hits the Back button
        #'''After incrementing the choice count, the code returns an HttpResponseRedirect rather than a normal HttpResponse.
        #HttpResponseRedirect takes a single argument: the URL to which the user will be redirected
        #(see the following point for how we construct the URL in this case).
        # As the Python comment above points out, you should always return an HttpResponseRedirect after successfully dealing
        # with POST data. This tip isn’t specific to Django; it’s just good Web development practice.'''
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
