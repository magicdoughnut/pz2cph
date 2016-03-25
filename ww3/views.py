from django.shortcuts import render
from django.http import HttpResponse
#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

def map_disp(request, latlon):
    #return render(request, 'map/map_disp.html', {})
    from mysite.settings import PROJECT_PATH
    from datetime import datetime, timedelta
    #np.save(PROJECT_PATH+'/../map/scratch/question_id.npy', question_id)

    file = open(PROJECT_PATH+'/../ww3/scratch/latlon.txt', "w")
    file.write(latlon[0:8]+'\n')
    file.write(latlon[8:10])   
    file.close()

       # Make a start datetime
    start = (datetime.now() - timedelta(days=10)).replace(hour=6, minute=0, second=0)

    # Make your datetimes
    dts = []
    for i in range(0, 10):

        # Move forward
        start += timedelta(hours=6)

        dts.append({'link': start.strftime('%Y%m%d%H'), 'prettyTime': start.strftime('%d-%m-%Y %H-%M-%S')})
    print(dts)
    return render(request, 'ww3/map_disp.html', dts)



def index(request):
    return HttpResponse("Here put some instructions on how to use the site (through the search window).")


def plotResults(request):
    # basic NOMADS OpenDAP extraction and plotting script
    from mysite.settings import PROJECT_PATH
    #from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from mpl_toolkits.basemap import Basemap
    import numpy as np
    import numpy.ma as ma
    import matplotlib.pyplot as plt
    import netCDF4
    import os.path
    
    # set up the URL to access the data server.
    # See the NWW3 directory on NOMADS 
    # for the list of available model run dates.
    
    file = open(PROJECT_PATH+'/../ww3/scratch/latlon.txt', "r")
    mydate = file.readline()
    mydate = mydate[0:-1]
    mytime = file.readline()
    file.close()

    if os.path.isfile(PROJECT_PATH+'/../ww3/scratch/images/'+mydate+mytime+'.png'):
            image_file = open(PROJECT_PATH+'/../ww3/scratch/images/'+mydate+mytime+'.png','rb').read()
    else:

        # set up the figure
        fig = plt.figure()

        #mydate='20160312'
        print(mydate)
        url='http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'+mydate+'/nww3'+mydate+'_'+mytime+'z'
        print(url)
        
        # Extract the significant wave height of combined wind waves and swell
        
        file = netCDF4.Dataset(url)
        lat  = file.variables['lat'][:]
        lon  = file.variables['lon'][:]
        data = file.variables['htsgwsfc'][1,:,:]
        file.close()
    

    
        split_point = lon.size/2

        data1 = data[:,0:split_point]
        data2 = data[:,split_point:288]
        new_data = ma.concatenate([data2, data1], axis=1)
    
        data = new_data
    
        a = float(360)/float(288)
        lon = np.arange(-180,180,a)
        
        # Since Python is object oriented, you can explore the contents of the NOMADS
        # data set by examining the file object, such as file.variables.
    
        # The indexing into the data set used by netCDF4 is standard python indexing.
        # In this case we want the first forecast step, but note that the first time 
        # step in the RTOFS OpenDAP link is all NaN values.  So we start with the 
        # second timestep
    
        # Plot the field using Basemap.  Start with setting the map
        # projection using the limits of the lat/lon data itself:
        
        #m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
        #    urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
        #    resolution='c')

        m=Basemap(projection='mill',lat_ts=10,llcrnrlon=-25, \
            urcrnrlon=20,llcrnrlat=40,urcrnrlat=65, \
            resolution='l')

        # convert the lat/lon values to x/y projections.
    
        x, y = m(*np.meshgrid(lon,lat))
    
        # plot the field using the fast pcolormesh routine 
        # set the colormap to jet.
        
        m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)
        m.colorbar(location='right')
    
        # Add a coastline and axis values.
    
        m.drawcoastlines()
        m.fillcontinents()
        m.drawmapboundary()
        m.drawparallels(np.arange(-90.,120.,10.),labels=[1,0,0,0])
        m.drawmeridians(np.arange(-180.,180.,10.),labels=[0,0,0,1])
        
        # Add a colorbar and title, and then show the plot.
    
        plt.title('NWW3 Significant Wave Height from NOMADS: '+mydate+' '+mytime+' Hours')

        fig.savefig(PROJECT_PATH+'/../ww3/scratch/images/'+mydate+mytime+'.png')

        image_file = open(PROJECT_PATH+'/../ww3/scratch/images/'+mydate+mytime+'.png','rb').read()

    return HttpResponse(image_file,content_type='image/png')




        #canvas = FigureCanvas(fig)
        #response = HttpResponse(content_type='image/png')
        
        #canvas.print_png(response)
        #return response
