"""
    Loads colorshemes are of length 101 to match percentile scores 0-100

    1. loads all Color Brewer schemes of 9 bin colors
    2. load custom 18 bin colorshemes based on two 9 bins schems plus grey

    return json of name2csid, for frontend user coloring options and testing
"""
import simplejson
import os,sys

if __name__=='__main__':
    sys.path.append("../../../dynTM/src/pyClient")
else: #relative paths are relative to the main script, so above breaks
    _this_dir = os.path.split(__file__)[0]
    sys.path.append(os.path.join(_this_dir, "../../../dynTM/src/pyClient"))

import DynTM

# make a client instance
AccessKeyID = 'dtmUser'
AccessKey = 'key'
border = True
client=DynTM.GeoDaWS_DynTM(AccessKeyID=AccessKeyID,AccessKey=AccessKey)

def make_array_colors(bins,colors, reverse=False): 
    """
    these color schemes will only work with classificationlists of values from 0-100 
    """
    assert len(bins)==len(colors), "bins and colors must be same length" 
    array_of_colors=[0]*101 # classlists always will be ints ranging 0 and 100
    for i,binn in enumerate(bins):
        minn=binn[0]
        maxx=binn[1]
        if reverse==False:
            color=colors[i]
        else:
            color=colors[-1*i]
        array_of_colors[minn:maxx+1]=[color]*(maxx-minn+1)
    assert (0 not in array_of_colors) == True
    return array_of_colors


## min, max
bins_9  =[[  90, 100],
           [ 80, 89],
           [ 70, 79],
           [ 60, 69],
           [ 40, 59],
           [ 30, 39],
           [ 20, 29],
           [ 10, 19],
           [ 0,  9 ]]


colorbrewer = {
        "YlGn":["#ffffe5","#f7fcb9","#d9f0a3","#addd8e","#78c679","#41ab5d","#238443","#006837","#004529"],
        "YlGnBu":["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"],
        "GnBu":["#f7fcf0","#e0f3db","#ccebc5","#a8ddb5","#7bccc4","#4eb3d3","#2b8cbe","#0868ac","#084081"],
        "BuGn":["#f7fcfd","#e5f5f9","#ccece6","#99d8c9","#66c2a4","#41ae76","#238b45","#006d2c","#00441b"],
        "PuBuGn":["#fff7fb","#ece2f0","#d0d1e6","#a6bddb","#67a9cf","#3690c0","#02818a","#016c59","#014636"],
        "PuBu":["#fff7fb","#ece7f2","#d0d1e6","#a6bddb","#74a9cf","#3690c0","#0570b0","#045a8d","#023858"],
        "BuPu":["#f7fcfd","#e0ecf4","#bfd3e6","#9ebcda","#8c96c6","#8c6bb1","#88419d","#810f7c","#4d004b"],
        "RdPu":["#fff7f3","#fde0dd","#fcc5c0","#fa9fb5","#f768a1","#dd3497","#ae017e","#7a0177","#49006a"],
        "PuRd":["#f7f4f9","#e7e1ef","#d4b9da","#c994c7","#df65b0","#e7298a","#ce1256","#980043","#67001f"],
        "OrRd":["#fff7ec","#fee8c8","#fdd49e","#fdbb84","#fc8d59","#ef6548","#d7301f","#b30000","#7f0000"],
        "YlOrRd":["#ffffcc","#ffeda0","#fed976","#feb24c","#fd8d3c","#fc4e2a","#e31a1c","#bd0026","#800026"],
        "YlOrBr":["#ffffe5","#fff7bc","#fee391","#fec44f","#fe9929","#ec7014","#cc4c02","#993404","#662506"],
        "Purples":["#fcfbfd","#efedf5","#dadaeb","#bcbddc","#9e9ac8","#807dba","#6a51a3","#54278f","#3f007d"],
        "Blues":["#f7fbff","#deebf7","#c6dbef","#9ecae1","#6baed6","#4292c6","#2171b5","#08519c","#08306b"],
        "Greens":["#f7fcf5","#e5f5e0","#c7e9c0","#a1d99b","#74c476","#41ab5d","#238b45","#006d2c","#00441b"],
        "Oranges":["#fff5eb","#fee6ce","#fdd0a2","#fdae6b","#fd8d3c","#f16913","#d94801","#a63603","#7f2704"],
        "Reds":["#fff5f0","#fee0d2","#fcbba1","#fc9272","#fb6a4a","#ef3b2c","#cb181d","#a50f15","#67000d"],
        "Greys":["#ffffff","#f0f0f0","#d9d9d9","#bdbdbd","#969696","#737373","#525252","#252525","#000000"],
        "PuOr":["#b35806","#e08214","#fdb863","#fee0b6","#f7f7f7","#d8daeb","#b2abd2","#8073ac","#542788"],
        "BrBG":["#8c510a","#bf812d","#dfc27d","#f6e8c3","#f5f5f5","#c7eae5","#80cdc1","#35978f","#01665e"],
        "PRGn":["#762a83","#9970ab","#c2a5cf","#e7d4e8","#f7f7f7","#d9f0d3","#a6dba0","#5aae61","#1b7837"],
        "PiYG":["#c51b7d","#de77ae","#f1b6da","#fde0ef","#f7f7f7","#e6f5d0","#b8e186","#7fbc41","#4d9221"],
        "RdBu":["#b2182b","#d6604d","#f4a582","#fddbc7","#f7f7f7","#d1e5f0","#92c5de","#4393c3","#2166ac"],
        "RdGy":["#b2182b","#d6604d","#f4a582","#fddbc7","#ffffff","#e0e0e0","#bababa","#878787","#4d4d4d"],
        "RdYlBu":["#d73027","#f46d43","#fdae61","#fee090","#ffffbf","#e0f3f8","#abd9e9","#74add1","#4575b4"],
        "Spectral":["#d53e4f","#f46d43","#fdae61","#fee08b","#ffffbf","#e6f598","#abdda4","#66c2a5","#3288bd"],
        "RdYlGn":["#d73027","#f46d43","#fdae61","#fee08b","#ffffbf","#d9ef8b","#a6d96a","#66bd63","#1a9850"],
        "Paired":["#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6"],
        "Pastel1":["#fbb4ae","#b3cde3","#ccebc5","#decbe4","#fed9a6","#ffffcc","#e5d8bd","#fddaec","#f2f2f2"],
        "Set1":["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#ffff33","#a65628","#f781bf","#999999"],
        "Set3":["#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9"]
        }


bins_19 = [[ 95, 100,"#00441b"],  # dark green
           [ 90, 95,"#006d2c"],
           [ 85, 90,"#238b45"],
           [ 80, 85,"#41ae76"],
           [ 75, 80,"#66c2a4"],
           [ 70, 75,"#99d8c9"],
           [ 65, 70,"#ccece6"],
           [ 60, 65,"#e5f5f9"],
           [ 55, 60,"#f7fcfd"],  # light green
           [ 45, 55,"#ffffff"],  # grey 
           [ 40, 45,"#fff5f0"],  # light red
           [ 35, 40,"#fee0d2"],
           [ 30, 35,"#fcbba1"],
           [ 25, 30,"#fc9272"],
           [ 20, 25,"#fb6a4a"],
           [ 15, 20,"#ef3b2c"],
           [ 10, 15,"#cb181d"],
           [ 5,  10,"#a50f15"],
           [ 0,  5 ,"#67000d" ]] # dark red

highlows=   [
            ["Greens","Reds"],
            ["Purples","Oranges"]
            ]

def flip(L):
    # flip high color sequence since initially  appear as light to dark
    # but bins go from high to low
    return L[::-1]

def make19binScheme(high_color,low_color): 
    grey = [ "#ffffff"]
    return flip(colorbrewer[high_color]) + grey + colorbrewer[low_color]

if __name__ == '__main__':
    name2csid={}
    for name, colors in colorbrewer.items():
        array_of_colors=make_array_colors(bins_9,flip(colors))
        csid = client.createColorScheme(array_of_colors) # load to simpleDB 
        name2csid[name]=csid


    for p in highlows:
        highcolor=p[0]
        lowcolor=p[1]
        combined=make19binScheme(highcolor,lowcolor)
        print combined
        array_of_colors=make_array_colors(bins_19, combined)
        csid = client.createColorScheme(array_of_colors) # load to simpleDB 
        name2csid[highcolor+lowcolor]=csid

    # pretty print json options used below
    json=simplejson.dumps(name2csid,sort_keys=True,indent=4, separators=(',', ': '))
    print "writing json of name2csid"
    print json
    f=open("name2csid.json","w")
    f.write(json)
    f.close
