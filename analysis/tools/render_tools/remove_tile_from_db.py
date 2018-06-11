"""
From shell manage simpleDB to remove tiles

USAGE: $ipython -i remove_tile_from_db.py

- removes tile from simpleDB cache for testing
"""
import sys,os
sys.path.append('/usr/local/django')
os.environ['DJANGO_SETTINGS_MODULE']='gws_sqlite.settings'
sys.path.append("../src/pyClient")
import geodaWebServices.dyntm.models
geodaWebServices.dyntm.models.Tile._install()
geodaWebServices.dyntm.models.TileSet._install()
geodaWebServices.dyntm.models.Classification._install()
geodaWebServices.dyntm.models.ColorScheme._install()

import geodaWebServices.shapeManager.models
geodaWebServices.shapeManager.models.Shapefile._install()

import geodaWebServices.geodaWebServiceAuth.models
geodaWebServices.geodaWebServiceAuth.models.GWS_User._install()
geodaWebServices.geodaWebServiceAuth.models.GWS_AccessKey._install()


from geodaWebServices.geodaWebServiceAuth import models
passwd = "test"
user = models.GWS_User.get('dtmUser')
if not user:
    user = models.create_gws_user('dtmUser',passwd)
else:
    user.set_password(passwd)
    user.put()
#key = models.create_accesskey(user)
key = models.GWS_AccessKey('dtmUser')
key.accessKey = "key"
key.user = user.username
key.put()
 
import DynTM
import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)
mc.flush_all()

AccessKeyID = 'dtmUser'
AccessKey = 'key'
md5="59DC0A533A2710CCF56FF68ED44C3CFF" # MEEGE 3.7GB
#md5="B02AA19D718648CEE35F97FE4BB980BC" # CA 
tsid=AccessKeyID+":"+md5
# DELETE TILE
t = geodaWebServices.dyntm.models.Tile.get('t:'+md5+':0+0+0')
t.delete()
client = DynTM.GeoDaWS_DynTM(AccessKeyID=AccessKeyID,AccessKey=AccessKey)
print "render tile 1st time: 45 seconds when not spaptially indexed"
x = 3
y = 2
z = 3

with open('output/'+md5+'.png','wb') as o:
    png = client.getTile(tsid, z, x, y)
    o.write(png)
