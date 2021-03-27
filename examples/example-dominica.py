import pystare
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import cartopy.crs as ccrs
import numpy

def plot1(lon=None,lat=None,lons=None,lats=None,triang=None,c0='r',c1='b',transf=None,lw=1,ax=None):
    if(lon is not None and ax is not None):
        x=np.zeros([lon.size+1],dtype=np.double);x[:-1]=lon[:];x[-1]=lon[0]
        y=np.zeros([lat.size+1],dtype=np.double); y[:-1]=lat[:]; y[-1]=lat[0]
        ax.plot(x,y,True,transform=transf,c=c0)
    ax.triplot(triang,c1+'-',transform=transf,lw=lw,markersize=3)
    ax.scatter(lons,lats,s=10,c=c1,transform=ccrs.PlateCarree())
    return

def plot2(sids,c0='r',c1='g',transf=None,ax=None):
    lons,lats,intmat = pystare.triangulate_indices(sids)
    triang = tri.Triangulation(lons,lats,intmat)
    plot1(None,None,lons=lons,lats=lats,triang=triang,c0=c0,c1=c1,transf=transf,lw=1,ax=ax)
    return

def dominica1(proj,transf):
    "Example and analysis for pystare bug#27."

    sids = numpy.array([2521898143583305738, 2521997099629805578, 2521989952804225034,
       2521991052315852810, 2521893745536794634, 2521897044071677962,
       2521897593827491850, 2521898693339119626, 2521899792850747402,
       2521991602071666698, 2521889347490283530, 2521899243094933514,
       2521900892362375178, 2521901442118189066, 2521901991874002954,
       2521903091385630730, 2521887698222841866, 2521886048955400202,
       2521992701583294474, 2521902541629816842, 2521906389920514058,
       2521890447001911306, 2521993251339108362, 2521886598711214090,
       2521908588943769610, 2521892646025166858, 2521894295292608522,
       2521989403048411146])

    sids = numpy.array([2521902129312956427, 2521902404190863371, 2521899930289700875,
       2521900067728654347, 2521900205167607819, 2521991876949573643,
       2521992701583294475, 2521992839022247947, 2521992976461201419,
       2521997099629805579, 2521889484929237003, 2521991739510620171,
       2521902679068770315, 2521908726382723083, 2521894432731561995,
       2521901579557142539, 2521989952804225035, 2521990365121085451,
       2521991327193759755, 2521997237068759051, 2521997511946665995,
       2521898418461212683, 2521898555900166155, 2521898693339119627,
       2521889759807143947, 2521903091385630731, 2521901716996096011,
       2521897456388538379, 2521902266751909899, 2521897868705398795,
       2521898968217026571, 2521990227682131979, 2521889622368190475,
       2521901167240282123, 2521887973100748811, 2521902816507723787,
       2521892920903073803, 2521894020414701579, 2521890721879818251,
       2521993526217015307, 2521901304679235595, 2521901854435049483,
       2521902953946677259, 2521898006144352267, 2521890859318771723,
       2521886461272260619, 2521888110539702283, 2521898830778073099,
       2521903228824584203, 2521897044071677963, 2521903366263537675,
       2521899105655980043, 2521903503702491147, 2521886048955400203,
       2521991602071666699, 2521899380533886987, 2521890584440864779,
       2521992014388527115, 2521886873589121035, 2521887011028074507,
       2521889347490283531, 2521890447001911307, 2521886736150167563,
       2521893745536794635, 2521893882975748107, 2521894157853655051,
       2521897181510631435, 2521897731266445323, 2521899792850747403,
       2521887698222841867, 2521900892362375179, 2521901442118189067,
       2521906389920514059, 2521908588943769611, 2521901991874002955,
       2521902541629816843, 2521909001260630027, 2521989540487364619,
       2521897318949584907, 2521898143583305739, 2521898281022259211,
       2521897593827491851, 2521993113900154891, 2521993251339108363,
       2521993388778061835, 2521993663655968779, 2521886598711214091,
       2521886186394353675])

    expanded_stare_test = numpy.array([
        0x22ff8a000000000b,
        0x22ff8a200000000b,
        0x22ff8a600000000b,
        0x22ff8a800000000b,
        0x22ff8aa00000000b,
        0x22ff8ac00000000b,
        0x22ff8ae00000000b,
        0x22ff8b800000000b,
        0x22ff8bc00000000b,
        0x22ff8be00000000b,
        0x22ff8d000000000a,
        0x22ff8e000000000a,
        0x22ff90400000000b,
        0x22ff91000000000a,
        0x22ff91a00000000b,
        0x22ff940000000009,
        0x22ff96200000000b,
        0x22ff96800000000a,
        0x22ff97800000000b,
        0x22ff97c00000000b,
        0x22ff97e00000000b,
        0x22ff980000000009,
        0x22ff9c800000000b,
        0x22ff9e800000000b,
        0x22ff9ea00000000b,
        0x22ff9ee00000000b,
        0x22ffe8200000000b,
        0x22ffe8800000000b,
        0x22ffe8c00000000b,
        0x22ffe8e00000000b,
        0x22ffe9c00000000b,
        0x22ffea000000000a,
        0x22ffeb000000000a,
        0x22ffeb800000000a,
        0x22ffef000000000b,
        0x22ffef200000000b,
        0x22ffef600000000b
        ])
    
    expanded_stare_test = numpy.array([
        0x22ff8a000000000b,
        0x22ff8a200000000b,
        0x22ff8a600000000b,
        0x22ff8a800000000a,
        0x22ff8b000000000a,
        0x22ff8b800000000a,
        0x22ff8b800000000b,
        0x22ff8bc00000000b,
        0x22ff8be00000000b,
        0x22ff8c0000000009,
        0x22ff8d000000000a,
        0x22ff8e0000000009,
        0x22ff8e000000000a,
        0x22ff900000000008,
        0x22ff90400000000b,
        0x22ff91000000000a,
        0x22ff91a00000000b,
        0x22ff940000000009,
        0x22ff96200000000b,
        0x22ff96800000000a,
        0x22ff97800000000b,
        0x22ff97c00000000b,
        0x22ff97e00000000b,
        0x22ff980000000008,
        0x22ff980000000009,
        0x22ff9c800000000b,
        0x22ff9e800000000b,
        0x22ff9ea00000000b,
        0x22ff9ee00000000b,
        0x22ffa00000000007,
        0x22ffc00000000007,
        0x22ffe00000000007,
        0x22ffe8200000000b,
        0x22ffe8800000000b,
        0x22ffe8c00000000b,
        0x22ffe8e00000000b,
        0x22ffe9c00000000b,
        0x22ffea000000000a,
        0x22ffeb000000000a,
        0x22ffeb800000000a,
        0x22ffef000000000b,
        0x22ffef200000000b,
        0x22ffef600000000b
        ])

    print('compressed = pystare.to_compressed_range(sids)')
    k = 0
    for i in sids:
        print(k,hex(i))
        k += 1
    print('')
    
    compressed = pystare.to_compressed_range(sids)
    print('compressed = pystare.to_compressed_range(sids)')
    k = 0
    for i in compressed:
        print(k,hex(i))
        k += 1
    print('')
    
    expanded = pystare.expand_intervals(compressed,-1,False)    
    print('expanded = pystare.expand_intervals(compressed,-1,False)')
    k = 0
    for i in expanded:
        print(k,hex(i))
        k += 1
    print('')

    expanded_mr = pystare.expand_intervals(compressed,-1,True)    
    print('expanded = pystare.expand_intervals(compressed,-1,True)')
    k = 0
    for i in expanded_mr:
        print(k,hex(i))
        k += 1
    print('')

    fig, axs = plt.subplots(nrows=1,ncols=5,subplot_kw={'projection':proj,'transform':transf})
    # plt.figure()
    # plt.subplot(projection=proj,transform=transf)

    iax=0
    
    ax=axs[iax]
    # ax.set_global()
    ax.coastlines()
    ax.title.set_text('1. Original\n(res=0xA)')
    ax.annotate(
        '1. sids\n2. compressed = pystare.to_compressed_range(sids) # Intervals. Terminators expressed as dots.\n3. expanded = pystare.expand_intervals(compressed,-1,False) # Intervals expanded according to embedded resolution.\n4. expanded_multires = pystare.expand_intervals(compressed,-1,True) # Intervals expanded into coarsest common ancestors.',
        xy=(50, 50), xycoords='figure pixels')
    plot2(sids,c0='r',c1='b',transf=transf,ax=ax)
    iax += 1

    ax=axs[iax]
    # ax.set_global()
    ax.coastlines()
    ax.title.set_text('2. Compressed\n(Incorrect usage)')
    plot2(compressed,c0='r',c1='b',transf=transf,ax=ax)
    iax += 1

    ax=axs[iax]
    # ax.set_global()
    ax.coastlines()
    ax.title.set_text('3. Expand Compressed\n(mono-res)')    
    plot2(expanded,c0='r',c1='b',transf=transf,ax=ax)
    iax += 1
    
    ax=axs[iax]
    # ax.set_global()
    ax.coastlines()
    ax.title.set_text('4. Expand Compressed\n(multi-res)')    
    plot2(expanded_mr,c0='r',c1='b',transf=transf,ax=ax)
    iax += 1

    ax=axs[iax]
    # ax.set_global()
    ax.coastlines()
    ax.title.set_text('5. Expand Compressed\n(multi-res)\nfrom STARE lib tests')    
    plot2(expanded_stare_test,c0='r',c1='b',transf=transf,ax=ax)
    iax += 1    
     
    plt.show()
    
    

#    compressed = pystare.to_compressed_range(flat_list) 
#    compressed.size
#    22
#    we get
#
#    array([2521886048955400202, 2521887148467027967, 2521887698222841866,
#        2521889347490283530, 2521890447001911306, 2521892646025166858,
#    2521893745536794634, 2521894845048422399, 2521897044071677961,
#    2521899243094933514, 2521900342606561279, 2521900892362375178,
#    2521903641141444607, 2521906389920514058, 2521908588943769610,
#    2521989403048411146, 2521990502560038911, 2521991052315852810,
#    2521992151827480575, 2521992701583294474, 2521993801094922239,
#               2521997099629805578])    
    
    return

def main():
    print('example-dominica')

    proj   = ccrs.PlateCarree()
    # transf = ccrs.Geodetic()
    transf = ccrs.PlateCarree()

    dominica1(proj,transf)

    return

if __name__ == '__main__':
    main()
