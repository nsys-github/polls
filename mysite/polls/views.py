from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
# Django では、汎用ビュー（generic view）というショートカットを提供
from django.utils import timezone

from .models import Choice, Question


"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #get_list_or_404()はfileter()を使います

    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # デフォルトでは、ListView 汎用ビューは <app name>/<model name>_list.html というデフォルトのテンプレートを使う

    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    # デフォルトでは、 DetailView 汎用ビューは <app name>/<model name>_detail.html という名前のテンプレートを使います。
    # template_name 属性を指定すると、指定したテンプレート名を使う

    # DetailView には、 question という変数が自動的に渡されます。なぜなら、 Django モデル (Question) を使用しているからです。

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # request.POST は辞書のようなオブジェクトです。キーを指定すると、送信したデータにアクセスできます。
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # POST データが成功した後は常に HttpResponseRedirect を返す必要があります。
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
