from django.shortcuts import render
from django.http import HttpResponse

#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

def map_disp(request):
    return render(request, 'map/map_disp.html', {})

def showStaticImage(request):
    """ Simply return a static image as a png """
    
    imagePath = "/Users/markdawson/Documents/python/pz2cph_workspace/mysite/map/staticImage.png"
    from PIL import Image
    Image.init()
    i = Image.open(imagePath)
    
    response = HttpResponse(mimetype='image/png')
    i.save(response,'PNG')
    return response