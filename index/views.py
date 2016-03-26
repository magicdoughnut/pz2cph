from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
	from mysite.settings import PROJECT_PATH
	return render(request, 'index/map_disp.html', {})
