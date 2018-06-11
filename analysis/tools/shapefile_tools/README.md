### Create a TileSet (a.k.a. A Shapefile)

    import sys
    sys.path.append("../src/pyClient")
    import DynTM

    YOUR-SHAPEFILE=<PATH-YOUR-SHAPEFILE>
    AccessKeyID = 'dtmUser'
    AccessKey = 'key'

    client = DynTM.GeoDaWS_DynTM(AccessKeyID=AccessKeyID,AccessKey=AccessKey)
    with open(YOUR-SHAPEFILE+'.shp','rb') as shp:
        with open(YOUR-SHAPEFILE+'.shx','rb') as shx:
            tsid = client.createTileSet(shp, shx)
    print "TSID:",tsid


`tsid` (Tile Set ID) is IMPORTANT, you put it into your HTML file to get map
tiles.
