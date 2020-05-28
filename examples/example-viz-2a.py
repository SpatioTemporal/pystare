
from math import ceil
import pystare as ps

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import cartopy.crs as ccrs

import numpy as np

def shiftarg_lon(lon):
    "If lon is outside +/-180, then correct back."
    if(lon>180):
        return ((lon + 180.0) % 360.0)-180.0
    else:
        return lon

def triangulate1(lats,lons):
    "Prepare data for tri.Triangulate."
    print('triangulating1...')
    intmat=[]
    npts=int(len(lats)/3)
    k=0
    for i in range(npts):
        intmat.append([k,k+1,k+2])
        k=k+3
    for i in range(len(lons)):
        lons[i] = shiftarg_lon(lons[i])
    print('triangulating1 done.')      
    return lons,lats,intmat

def plot1(lon,lat,lons,lats,triang,c0='r',c1='b',transf=None,lw=1):
    # if(lon is not None):
    if True:
        x=np.zeros([lon.size+1],dtype=np.double);x[:-1]=lon[:];x[-1]=lon[0]
        y=np.zeros([lat.size+1],dtype=np.double); y[:-1]=lat[:]; y[-1]=lat[0]
        ax.plot(x,y,True,transform=transf,c=c0)
    plt.triplot(triang,c1+'-',transform=transf,lw=lw,markersize=3)
    # plt.scatter(lons,lats,s=10,c=c1,transform=transf)
    return

def make_hull(lat0,lon0,resolution0):
    hull0 = ps.to_hull_range_from_latlon(lat0,lon0,resolution0)
    print('hull0 len: ',len(hull0),type(hull0))
    lath0,lonh0,lathc0,lonhc0 = ps.to_vertices_latlon(hull0)
    lons0,lats0,intmat0 = ps.triangulate(lath0,lonh0)
    print('lons0  len: ',len(lons0))
    print('intmat len: ',len(intmat0),type(intmat0))
    triang0 = tri.Triangulation(lons0,lats0,intmat0)
    for i in range(len(intmat0)):
        print(i,intmat0[i],lons0[intmat0[i]],lats0[intmat0[i]])
    print('triang ',triang0.triangles.shape)
    # exit()
    return lats0,lons0,triang0,hull0

# resolution = 5
# resolution = 4
resolution = 3

resolution0 = resolution;

# lat0 = np.array([ 10, 5, 60,70], dtype=np.double)
# lon0 = np.array([-30,-20,60,10], dtype=np.double)

lat0 = np.array([0, 0,10,10], dtype=np.double)
lon0 = np.array([0,20,20,0], dtype=np.double)

lats0,lons0,triang0,hull0 = make_hull(lat0,lon0,resolution0)
print('hull0: ',len(hull0))

# Set up the projection and transformation
proj = ccrs.PlateCarree()
# proj = ccrs.Robinson() # Drives spurious IllegalArgumentException: Argument must be Polygonal or LinearRing
# proj   = ccrs.Mollweide() # Drives spurious IllegalArgumentException: Argument must be Polygonal or LinearRing
transf = ccrs.Geodetic()
# transf = ccrs.PlateCarree()
plt.figure()
plt.subplot(projection=proj,transform=transf)
ax = plt.axes(projection=proj,transform=transf)
ax.set_global()
ax.coastlines()
print('graphics-0')
plot1(lon0,lat0,lons0,lats0,triang0,c0='r',c1='b',transf=transf)
plt.show()
