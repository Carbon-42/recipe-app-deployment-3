from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import RecipeSearchForm
import pandas as pd
from .utils import get_chart

# Create your views here.


def home(request):
    return render(request, 'recipes/recipes_home.html')


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/main.html'


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'


# KEEP PROTECTED

@login_required
def records(request):
    # create an instance of SalesSearchForm that you defined in sales/forms.py
    form = RecipeSearchForm(request.POST or None)
    diff_df = None  # intialize dataframe as None
    chart = None

    # check if the button is clicked
    if request.method == 'POST':
        # read book_title and chart_type
        recipe_diff = request.POST.get('recipe_diff')
        chart_type = request.POST.get('chart_type')
        # display in terminal - needed for debugging during development only
        # print(recipe_diff, chart_type)

        if recipe_diff == '#1':
            recipe_diff = 'Easy'
        if recipe_diff == '#2':
            recipe_diff = 'Medium'
        if recipe_diff == '#3':
            recipe_diff = 'Intermediate'
        if recipe_diff == '#4':
            recipe_diff = 'Hard'

        qs = Recipe.objects.all()
        id_list = []
        for obj in qs:
            diff = obj.calc_difficulty()
            if diff == recipe_diff:
                id_list.append(obj.id)

        qs = qs.filter(id__in=id_list)
        print(qs)
        if qs:
            diff_df = pd.DataFrame(qs.values())

            links = []
            for i, name in enumerate(diff_df['name']):
                name = '<a href="/list/' + \
                    str(diff_df['id'][i]) + '" >' + str(name) + '</a >'
                links.append(name)

            chart = get_chart(chart_type, diff_df,
                              labels=diff_df['name'].values)

            diff_df['name'] = links
            diff_df = diff_df.to_html(index=False, escape=False)

     # pack up data to be sent to template in the context dictionary
    context = {
        'form': form,
        'diff_df': diff_df,
        'chart': chart,
    }

 # load the sales/record.html page using the data that you just prepared
    return render(request, 'recipes/records.html', context)
