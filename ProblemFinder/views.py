from django.http import HttpResponse
from django.template import loader
from .models import Question


# Create your views here.
def index(request):

    questions_list = Question.objects.order_by('title')
    template = loader.get_template('problemfinder/index.html')

    context = {
        'question_list' : questions_list
    }

    return HttpResponse(template.render(context, request))
