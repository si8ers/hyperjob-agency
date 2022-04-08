from vacancy.models import Vacancy
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django import forms


class VacancyView(View):
    def get(self, request):
        items = Vacancy.objects.all()
        return render(request, 'vacancy/list.html', context={'items': items})


class VacancyForm(forms.Form):
    description = forms.CharField(label='Description')


class VacancyViewNew(View):

    def get(self, request):
        form = VacancyForm(request.POST)
        user = request.user
        if not user.is_authenticated or not user.is_staff:
            return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
        return render(request, 'vacancy/new.html', context={'form': form})

    def post(self, request):
        form = VacancyForm(request.POST)
        user = request.user
        if not user.is_authenticated or not user.is_staff:
            return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
        if form.is_valid():
            data = form.cleaned_data
            v = Vacancy(description=data.get('description'), author=user)
            v.save()
            return redirect('/')

        return render(request, 'vacancy/new.html', context={'form': form})
