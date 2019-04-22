from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.views.decorators.csrf import csrf_exempt
from neo4j.v1 import GraphDatabase, basic_auth

import logging

class IndexView(generic.ListView):
    var = False
    template_name = 'polls/index1.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class WineView(generic.TemplateView):
    model = Question
    template_name = 'polls/wineresults.html'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
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
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def pickwine(request):
        var = True
        q1 = request.POST['q1']
        q2 = request.POST['q2']
        q3 = request.POST['q3']
        q4 = request.POST['q4']
        q5 = request.POST['q5']

        prices = q5.split(" to ")
        lower = int(prices[0])
        upper = int(prices[1])
        # query by current selection
        driver = GraphDatabase.driver(
            "bolt://localhost:7687", 
            auth=basic_auth("neo4j", "jesus"))
        session = driver.session()

        # 1 - Wine Variety
        # 2 - Country
        # 3 - Region
        # 4 - Winery
        # 5 - Price range
        cypher_query = '''
        MATCH (z:Winery)-[:MAKES]->(w:Wine)<-[d:DESCRIBES]-(r:Reviewer)
        WHERE z.wineryName = $winery AND w.variety = $variety AND
        z.country = $country AND z.region_1 = $region AND
        toInteger(w.price) >= $lower AND toInteger(w.price) <= $upper
        WITH w.variety as wine, z.wineryName as winery, w.price as price, z.country as country, z.region_1 as region
        RETURN wine, winery, price, country, region LIMIT 10
        '''

        results = session.run(cypher_query,
        parameters={"country": q2, "region": q3, "winery": q4, "variety": q1, "lower": lower, "upper": upper})
        
        wineries = list()
        countries = list()
        regions = list()
        wines = list()
        prices = list()

        for record in results:
            wineries.append(record["winery"])
            countries.append(record["country"])
            regions.append(record["region"])
            wines.append(record["wine"])
            prices.append(record["price"])

        if len(wineries) == 0:
            wineries.append("None Found")
            countries.append("None Found")
            regions.append("None Found")
            wines.append("None Found")
            prices.append("None Found")

        return render(request, 'polls/index1.html', {'results':var,'q1':wines[0], 'q2':countries[0], 'q3':regions[0], 'q4':wineries[0],'q5':prices[0]})
