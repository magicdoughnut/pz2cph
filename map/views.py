from django.shortcuts import render
from django.http import HttpResponse
from .forms import EmailForm
#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

def map_disp(request, latlon):
    #return render(request, 'map/map_disp.html', {})
    from mysite.settings import PROJECT_PATH
    #np.save(PROJECT_PATH+'/../map/scratch/question_id.npy', question_id)
    file = open(PROJECT_PATH+'/../map/scratch/latlon.txt', "w")
    file.write(latlon)
    file.close()
    return render(request, 'map/map_disp.html', {})

def index(request):
    return HttpResponse("Here put some instructions on how to use the site (through the search window).")

#def home(request):
#	form = EmailForm()
#	context = {"form": form}
#	template = "map_disp.html"
#	return render(request, template, context)

def plotResults(request):
    from mysite.settings import PROJECT_PATH
    #from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.basemap import Basemap

    
    #lat = int(input('latitude:	\n'))
    #lon = int(input('longitude:	\n'))
    #lat = 50

    #latlon = int(np.asscalar(np.load(PROJECT_PATH+'/../map/scratch/question_id.npy')))
    file = open(PROJECT_PATH+'/../map/scratch/latlon.txt', "r")
    latlon = file.readline()
    file.close()

    lat = int(latlon[0:2])
    lon = int(latlon[2:6])

    reduction = 100

    #data = np.loadtxt('/Users/markdawson/Documents/python/GEBCO2014_-15.0_48.0_10.0_65.0_30Sec_ESRIASCII.asc', skiprows=6)
    data_reduc = np.load(PROJECT_PATH+'/../map/scratch/data_reduc.npy')
    xg_reduc = np.load(PROJECT_PATH+'/../map/scratch/xg_reduc.npy')
    yg_reduc = np.load(PROJECT_PATH+'/../map/scratch/yg_reduc.npy')
    data_reduc = np.flipud(data_reduc)
    #x = np.arange(48,65,float(65-48)/3000)
    #y = np.arange(-15,10,float(25)/2040)
    
    #xg,yg = np.meshgrid(x,y)
    
    ##Reduce the number of data points
    #xg_reduc = xg[1:-1:reduction,0:-1:reduction]
    #yg_reduc = yg[1:-1:reduction,0:-1:reduction]
    #data_reduc = data[1:-1:reduction,0:-1:reduction]

    #Calculate closets data point in x direction (longitude)
    tmp = abs(xg_reduc[1,:]-lon)
    x_idx = np.argmin(tmp)
    
    #Calculate closets data point in y direction (latitude)
    tmp = abs(yg_reduc[:,1]-lat)
    y_idx = np.argmin(tmp)

        
    fig = plt.figure()

    m = Basemap(llcrnrlon=-20.,llcrnrlat=45.,urcrnrlon=15.,urcrnrlat=68.,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='merc',\
                lat_0=40.,lon_0=-20.,lat_ts=20.)

    x2, y2 = m(lon,lat)
    
    #xg2,yg2 = m(xg_reduc[1,x_idx],yg_reduc[y_idx,1])
    xg_reduc2 = np.reshape(xg_reduc, (1, np.size(xg_reduc)))
    yg_reduc2 = np.reshape(yg_reduc, (1, np.size(yg_reduc)))
    xg2,yg2 = m(yg_reduc2,xg_reduc2)
    
    xg3,yg3 = m(yg_reduc[y_idx,1],xg_reduc[1,x_idx])
    
    m.drawmapboundary(fill_color='#99ffff')
    m.fillcontinents(color='#cc9966',lake_color='#99ffff')
    m.scatter(xg2,yg2,1,marker='o',color='k')
    m.scatter(x2,y2,15,marker='o',color='r')
    m.scatter(xg3,yg3,2,marker='x',color='r')
    plt.annotate('Depth (MSL): \n'+str(data_reduc[x_idx,y_idx])+' m', xy=(-0.4, 0.8), xycoords='axes fraction')
    print('image saved')

    fig.savefig(PROJECT_PATH+'/../map/result.png')
    print('image saved')


    image_file = open(PROJECT_PATH+'/../map/result.png','rb').read()
    return HttpResponse(image_file,content_type='image/png')

    #return render(request, 'map/result.png', {})
    #canvas = FigureCanvas(fig)
    #response = HttpResponse(content_type='image/png')
    
    #canvas.print_png(response)
    #return response
    
#    #Plot
#    fig = plt.figure()
#    ax = fig.add_subplot(111, projection='3d')
#    ax.scatter(xg_reduc,yg_reduc,data_reduc)
#    ax.scatter(lon,lat,2000,c='r')
#    ax.scatter(xg_reduc[1,x_idx],yg_reduc[y_idx,1],1000,c='r')
#    #plt.show()
#
#    ax.view_init(90, 0)
#
#    #ax.grid(True)
#    canvas = FigureCanvas(fig)
#    response = HttpResponse(content_type='image/png')
#    
#    canvas.print_png(response)
#    return response


# def plotResults(request,poll_id):
#     import matplotlib
#     from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#     from matplotlib.figure import Figure
#     from matplotlib.dates import DateFormatter
#     fig = Figure()
    
#     ax=fig.add_subplot(1,1,1)
#     p = get_object_or_404(Poll, pk=poll_id) # Get the poll object from django
    
#     x = matplotlib.numpy.arange(1,p.choice_set.count())
#     choices = p.choice_set.all()
    
#     votes = [choice.votes for choice in choices]
#     names = [choice.choice for choice in choices]
    
    
#     numTests = p.choice_set.count()
#     ind = matplotlib.numpy.arange(numTests) # the x locations for the groups
    
#     cols = ['red','orange','yellow','green','blue','purple','indigo']*10
    
#     cols = cols[0:len(ind)]
#     ax.bar(ind, votes,color=cols)
    
    
#     ax.set_xticks(ind + 0.5)
#     ax.set_xticklabels(names)
    
    
#     ax.set_xlabel("Choices")
#     ax.set_ylabel("Votes")
    
#     #ax.set_xticklabels(names)
    
#     title = u"Dynamically Generated Results Plot for poll: %s" % p.question
#     ax.set_title(title)
    
    
#     #ax.grid(True)
#     canvas = FigureCanvas(fig)
#     response = HttpResponse(content_type='image/png')
    
#     canvas.print_png(response)
#     return response
