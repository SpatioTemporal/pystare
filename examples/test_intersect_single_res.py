
# Visualize test_intersect_single_res seen in test_intersections.py

import pystare
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import cartopy.crs as ccrs
import numpy

def plot1(lon,lat,lons,lats,triang,c0='r',c1='b',transf=None,lw=1,ax=None):
    if(lon is not None and ax is not None):
        x=np.zeros([lon.size+1],dtype=np.double);x[:-1]=lon[:];x[-1]=lon[0]
        y=np.zeros([lat.size+1],dtype=np.double); y[:-1]=lat[:]; y[-1]=lat[0]
        ax.plot(x,y,True,transform=transf,c=c0)
    ax.triplot(triang,c1+'-',transform=transf,lw=lw,markersize=3)
    ax.scatter(lons,lats,s=10,c=c1,transform=ccrs.PlateCarree())
    return

def test_intersect_single_res(proj,transf):
     resolution = 6
     resolution0 = resolution
     lat0 = numpy.array([ 10, 5, 60,70], dtype=numpy.double)
     lon0 = numpy.array([-30,-20,60,10], dtype=numpy.double)
     hull0 = pystare.to_hull_range_from_latlon(lat0, lon0, resolution0)

     lons0,lats0,intmat0 = pystare.triangulate_indices(hull0)
     triang0 = tri.Triangulation(lons0,lats0,intmat0)
     
     resolution1 = 6
     lat1 = numpy.array([10,  20, 30, 20 ], dtype=numpy.double)
     lon1 = numpy.array([-60, 60, 60, -60], dtype=numpy.double)
     hull1 = pystare.to_hull_range_from_latlon(lat1, lon1, resolution1)

     lons1,lats1,intmat1 = pystare.triangulate_indices(hull1)
     triang1 = tri.Triangulation(lons1,lats1,intmat1)

     fig, axs = plt.subplots(3,subplot_kw={'projection':proj,'transform':transf})
     # plt.figure()
     # plt.subplot(projection=proj,transform=transf)
     ax=axs[0]
     # ax.set_global()
     ax.coastlines()
     
     plot1(None,None,lons0,lats0,triang0,c0='r',c1='b',transf=transf,ax=ax)
     plot1(None,None,lons1,lats1,triang1,c0='c',c1='r',transf=transf,ax=ax)
     # plt.show()
     
     intersectedFalse = pystare.intersect(hull0, hull1, multiresolution=False)
     # print('intersectedFalse: ',intersectedFalse)
     
     intersectedTrue  = pystare.intersect(hull0, hull1, multiresolution=True)

     # plt.figure()
     # plt.subplot(projection=proj,transform=transf)
     ax=axs[1]
     # ax.set_global()
     ax.coastlines()

     lonsF,latsF,intmatF = pystare.triangulate_indices(intersectedFalse)
     triangF = tri.Triangulation(lonsF,latsF,intmatF)
     plot1(None,None,lonsF,latsF,triangF,c0='r',c1='b',transf=transf,ax=ax)
     # plt.show()

     # plt.figure()
     # plt.subplot(projection=proj,transform=transf)
     ax=axs[2]
     # ax.set_global()
     ax.coastlines()

     lonsT,latsT,intmatT = pystare.triangulate_indices(intersectedTrue)
     triangT = tri.Triangulation(lonsT,latsT,intmatT)
     plot1(None,None,lonsT,latsT,triangT,c0='r',c1='b',transf=transf,ax=ax)
     plt.show()

     # print('   len(False),len(True),delta: ',len(intersectedFalse),len(intersectedTrue),len(intersectedTrue)-len(intersectedFalse))
     # print('un len(False),len(True),delta: ',len(numpy.unique(intersectedFalse)),len(numpy.unique(intersectedTrue)),len(numpy.unique(intersectedTrue))-len(numpy.unique(intersectedFalse)))
     # print('compressed==True, first total, then w/o double counting: ',(7*16)+(17*4),(7*16)+(17*4)-(7+17))
     # print('count 0:    ',sum([1,34,34,4*6,24,22,9]))

def main():
    print('test_intersect_single_res.py visualization')

    proj   = ccrs.PlateCarree()
    # transf = ccrs.Geodetic()
    transf = ccrs.PlateCarree()

    test_intersect_single_res(proj,transf)

    return

if __name__ == '__main__':
    main()
