"""
pyGWS: Python clients for GeoDa Web Services

Author: Charles R Schmidt

Organization:
    The main package include general purpose utilities that are applicable to all GeoDa Web Services.
    Sub-packages contain the clients for individual web services.
"""
import urllib2
import urllib
from wsgiref.handlers import format_date_time
import time, base64, hmac, hashlib
import simplejson
import pyGWS
import array
import zlib,base64
import time
import math
import hashlib
import logging

UNSIGNED_ITEM_TYPES = {array.array('B').itemsize:'B', array.array('H').itemsize:'H', array.array('I').itemsize:'I', array.array('L').itemsize:'L'}
LARGE_FILE_SIZE = 50*1024*1024
LARGE_FILE_SIZE = 1
CHUNK_SIZE = 10*1024*1024
DEBUG = True

#logging.basicConfig(filename='dyntm-client.log',filemode='w',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s' ' | ' '%(filename)s' ' line:' '%(lineno)d',
                    filename='dyntm-client.log',
                    filemode='w',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logging.debug('dyntm-client logging is working')

HOST = "http://api.geoscore.com"

class DeleteRequest(urllib2.Request):
    def get_method(self):
        return "DELETE"
class PutRequest(urllib2.Request):
    def get_method(self):
        return "PUT"

class GeoDaWebServiceClient(object):
    _url="http://127.0.0.1:8000"
    def __init__(self,AccessKeyID=None, AccessKey=None):
        if not AccessKeyID:
            self.__AccessKeyID = ''
            self.__AccessKey = ''
        else:
            self.__AccessKeyID = AccessKeyID
            self.__AccessKey = AccessKey
        while self._url.endswith('/'):
            self._url = self._url[:-1]
    def _get(self,path,raiseErrors=False):
        return self._open(path,raiseErrors=raiseErrors)
    def _post(self,path,data,raiseErrors=False):
        return self._open(path,data,raiseErrors=raiseErrors)
    def _put(self,path,data,raiseErrors=False):
        return self._open(path,data,raiseErrors=raiseErrors,Request=PutRequest)
    def _delete(self,path,raiseErrors=False):
        return self._open(path,raiseErrors=raiseErrors,Request=DeleteRequest)
    def _open(self,path,data=None,raiseErrors=False,Request=urllib2.Request):
        url = "%s/%s"%(self._url,path)
        r = Request(url)
        if data:
            r.add_data(urllib.urlencode(data))
        r = sign_request(r,self.__AccessKeyID,self.__AccessKey)
        if DEBUG: print r.get_header("Authorization")
        try:
            print "path: ", path
            print "url: ", url
            print "r: ", r
            return urllib2.urlopen(r)
        except urllib2.HTTPError,e:
            if raiseErrors:
                raise
            else:
                return e
def sign_request(request,AccessKeyID,AccessKey,AuthType="GeoDaWS"):
    """ Signs a urllib2.Request and returns the signed Request Object

    Add the Authorization Header as such,
        Authorization: GeoDaWS AccessKeyID:Signature

    Signature = Base64( HMAC-SHA1( UTF-8-Encoding-Of( AccessKey,StringToSign ) ) )

    StringToSign =  HTTP-Verb + "\n" + 
                    Content-MD5 + "\n" +
                    Content-Type + "\n" +
                    Date + "\n" +
                    ResourceSelector

    ResourceSelector = "/path/to/resource"

    Example of StringToSign: "GET\n\ntext/plain\nThu, 01 Apr 2010 01:23:10 GMT\n/dict/user"

    Based on AWS REST Authentication: http://docs.amazonwebservices.com/AmazonS3/latest/index.html?RESTAuthentication.html
    """
    string2sign = "%(verb)s\n%(md5)s\n%(ctype)s\n%(date)s\n%(path)s"

    args = {'verb':'','md5':'','ctype':'','date':'','path':''}
    # HTTP-Verb
    args['verb'] = request.get_method() # HTTP-Verb
    # Content-MD5
    if not request.has_header('Content-md5') and request.has_data(): #Does not contain Content-MD5 header, but has data.
        md5 = hashlib.md5(request.get_data()).hexdigest() # Calc the data's MD5
        request.add_header('Content-md5',md5) # add the MD5 header
        args['md5'] = request.get_header('Content-md5')
    elif request.has_header('Content-md5'): #already has an md5 header
        args['md5'] = request.get_header('Content-md5')
    # Content-Type
    if not request.has_header("Content-type"):
        request.add_header("Content-type","text/plain")
    args['ctype'] = request.get_header("Content-type")
    # Date
    if not request.has_header("Date"):
        request.add_header("Date",format_date_time(time.time()))
    args['date'] = request.get_header('Date')
    # ResourceSelector
    args['path'] = urllib.quote(request.get_selector())

    if DEBUG: print "BEGIN STRING TO SIGN..."
    if DEBUG: print string2sign%args
    if DEBUG: print "END STRING TO SIGN."
    signature = base64.b64encode(hmac.new(AccessKey,(string2sign%args).encode('UTF-8'),hashlib.sha1).hexdigest())
    auth = "%s %s:%s"%(AuthType,AccessKeyID,signature)
    request.add_header('Authorization',auth)
    return request


class GeoDaWS_DynTM(pyGWS.GeoDaWebServiceClient):
    """
    Python Client for the Dynamic Tile Mapper Web Service.

    Example Usage:
    
    Open a connection...
    >>> AccessKeyID = 'testuser4c3e5149'
    >>> AccessKey = '753b191f8ba15595361c962899b90d009accee6a'
    >>> client = GeoDaWS_DynTM(AccessKeyID=AccessKeyID,AccessKey=AccessKey)

    Upload a new Shapefile...
    >>> shp = open("../../../example_data/stl_hom/stl_hom.shp",'rb')
    >>> shx = open("../../../example_data/stl_hom/stl_hom.shx",'rb')
    >>> result = client.createTileSet(shp,shx)
    >>> result == 'testuser:B9C118EB30A9EAE19C93902E9F01EF8A'
    True
    >>> time.sleep(0.5)

    Describe the New Shapefile....
    >>> result = client.describeTileSet('testuser:B9C118EB30A9EAE19C93902E9F01EF8A')['shpfile']
    >>> result == 'B9C118EB30A9EAE19C93902E9F01EF8A'
    True
    >>> time.sleep(0.5)

    Download a tile...
    >>> png = client.getTile('testuser:B9C118EB30A9EAE19C93902E9F01EF8A',5,7,12)
    >>> png[:4] == '\x89PNG'
    True
    >>> open('tst0.png','wb').write(png)

    Post a Classification...
    >>> cl = [3, 2, 2, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 2, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 3, 3, 3, 2, 2]
    >>> result = client.createClassification('testuser:B9C118EB30A9EAE19C93902E9F01EF8A',cl)
    >>> result == 'testuser:474f117491ba503bde2b1eb2b9a36b3a'
    True
    >>> time.sleep(0.5)

    List Classifications...
    >>> result = client.listClassifications()
    >>> 'testuser:474f117491ba503bde2b1eb2b9a36b3a' in result
    True
    >>> time.sleep(0.5)

    Download a classified tile...
    >>> png = client.getTile('testuser:B9C118EB30A9EAE19C93902E9F01EF8A',5,7,12,'testuser:474f117491ba503bde2b1eb2b9a36b3a')
    >>> png[:4] == '\x89PNG'
    True
    >>> open('tst1.png','wb').write(png)

    Upload a colorScheme...
    >>> colors = ['#00ff00','#0000ff']
    >>> result = client.createColorScheme(colors)
    >>> result == 'testuser:b0726a29f9068870b701650e7adae8f7'
    True
    >>> time.sleep(0.5)

    Download a classified colored tile...
    >>> png = client.getTile('testuser:B9C118EB30A9EAE19C93902E9F01EF8A',5,7,12,'testuser:474f117491ba503bde2b1eb2b9a36b3a','testuser:b0726a29f9068870b701650e7adae8f7')
    >>> png[:4] == '\x89PNG'
    True
    >>> open('tst2.png','wb').write(png)

    Delete a Classification...
    >>> client.deleteClassification('testuser:474f117491ba503bde2b1eb2b9a36b3a')
    True

    Delete a ColorSchme...
    >>> client.deleteColorScheme('testuser:b0726a29f9068870b701650e7adae8f7')
    True

    Delete a shapefile...
    >>> client.deleteTileSet('testuser:B9C118EB30A9EAE19C93902E9F01EF8A')
    True
    >>> time.sleep(0.5)
    >>> result = client.describeTileSet('testuser:B9C118EB30A9EAE19C93902E9F01EF8A')
    >>> result == {'error': 'TileSet Not Found'}
    True


    """
    _url=HOST+"/dyntm.json/"
    def __init__(self,AccessKeyID, AccessKey):
        pyGWS.GeoDaWebServiceClient.__init__(self,AccessKeyID,AccessKey)
    def createTileSet(self,shpfile,shxfile):
        """
        Post a new TileSet to the server.
        
        Parameters:
        shpfile -- an open file-like object containing the ".shp" file.
        shxfile -- an open file-like object containing the ".shx" file.

        Returns:
        tileSetID of the newly create TileSet if successful, otherwise false.

        Example:
        >>> AccessKeyID = 'testuser4c3e5149'
        >>> AccessKey = '753b191f8ba15595361c962899b90d009accee6a'
        >>> client = GeoDaWS_DynTM(AccessKeyID=AccessKeyID,AccessKey=AccessKey)
        >>> shp = open("../../../example_data/stl_hom/stl_hom.shp",'rb')
        >>> shx = open("../../../example_data/stl_hom/stl_hom.shx",'rb')
        >>> result = client.createTileSet(shp,shx)
        >>> result == 'testuser:B9C118EB30A9EAE19C93902E9F01EF8A'
        True
        >>> time.sleep(0.5)
        >>> client.deleteTileSet('testuser:B9C118EB30A9EAE19C93902E9F01EF8A')
        True
        """
        shpfile.seek(0,2)#EOF
        f_size = shpfile.tell()
        shpfile.seek(0)
        if f_size > (LARGE_FILE_SIZE):
            logging.debug("Large File: Uploading in parts...")
            return self.createTileSet_Chunks(shpfile,shxfile,f_size)
        data = {}
        #data['shpname'] = 'stl_hom'
        data['shp'] = base64.b64encode(zlib.compress(shpfile.read()))
        data['shx'] = base64.b64encode(zlib.compress(shxfile.read()))
        data['force'] = FORCE
        logging.debug(data.keys())
        logging.debug(data["force"])
        #data['dbf'] = base64.b64encode(zlib.compress(dbf.read()))
        url = self._post('tileset',data,raiseErrors=False)
        if url.code == 200:
            return simplejson.loads(url.read())['TileSetID']
        else:
            logging.debug("Server returned error code: ", url.code)
            return url
    def createTileSet_Chunks(self,shpfile,shxfile,shp_size):
        """
        Post a new TileSet to the server, by uploading the file in chunks.
        We'll use a multipart upload inspired by S3's new multipart upload feature.

        Parameters:
        shpfile -- an open file-like object containing the ".shp" file.
        shxfile -- an open file-like object containing the ".shx" file.

        Returns:
        tileSetID of the newly create TileSet if successful, otherwise false.
        """
        shpfile.seek(0)
        #calc MD5
        shpMD5 = hashlib.md5()
        dat = shpfile.read(2**16)
        while dat:
            logging.debug("reading in chuncks...")
            shpMD5.update(dat)
            dat = shpfile.read(2**16)
        shpfile.seek(0)

        #initiate upload
        data = {}
        data['shpmd5'] = shpMD5.hexdigest().upper()
        data['shx'] = base64.b64encode(zlib.compress(shxfile.read()))
        data['force'] = FORCE
        logging.debug("shpmd5", data['shpmd5'])
        logging.debug("force", data['force'])
        url = self._post('tileset',data,raiseErrors=False)
        if url.code == 200:
            result = simplejson.loads(url.read())
            logging.debug("Server response from tileset post: ", result)
            if "TileSetID" in result and FORCE==False:
                logging.debug("Large File: Already Exists on Server, No Upload needed. force==",FORCE)
                return result['TileSetID']
            elif "TileSetID" in result and FORCE==True:
                    logging.debug("Warning: servers logic broken since no upload yet force==", FORCE)
            else:
                logging.debug("Large file initializing multipart upload, MD5=",data['shpmd5'])
                del data['shx']
                parts = []
                data['uploadId'] = result['uploadId']
                data['partNum'] = 1
                data['shpPart'] = base64.b64encode(zlib.compress(shpfile.read(CHUNK_SIZE)))
                print "part size:", len(data['shpPart'])
                while data['shpPart']:
                    try:
                        t0 = time.time()
                        url = self._post('tileset',data,raiseErrors=False)
                        result = url.read()
                        logging.debug(result)
                        result = simplejson.loads(result)
                        t1 = time.time()
                        if result['etag']:
                            kbps = ((len(data['shpPart'])/1024.0)/(t1-t0))
                            print "Large File: Uploaded Part %d (%s): %0.2f kB/s"%(data['partNum'],result['etag'],kbps)
                            parts.append(result['etag'])
                            data['partNum']+=1
                            dat = shpfile.read(CHUNK_SIZE)
                            if dat:
                                data['shpPart'] = base64.b64encode(zlib.compress(dat))
                            else:
                                data['shpPart'] = ''
                        else:
                            "Part %d upload failed. Trying Again."%data['partNum']
                    except:
                        raise
                del data['shpPart']
                del data['partNum']
                data['partsList'] = ','.join(parts)
                url = self._post('tileset',data,raiseErrors=False)
                if url.code == 200:
                    print "Large File: Upload Complete"
                    return simplejson.loads(url.read())['TileSetID']
                else:
                    print "Server returned error code: %d"%(url.code)
                    return url
        else:
            print "Server returned error code: %d"%(url.code)
            return url
            
    def listTileSets(self):
        result = self._get('tileset',raiseErrors=False)
        if result.code == 200:
            return eval(result.read(),{},{})['tilesets']
        else:
            return None
    def describeTileSet(self,tileSetName):
        result = self._get('tileset/%s'%tileSetName).read()
        print result
        return simplejson.loads(result)
    def deleteTileSet(self,tileSetName):
        result = self._delete('tileset/%s'%tileSetName).read()
        return simplejson.loads(result)
    @staticmethod
    def getTile(tileSetID,zoom,x,y,clid=None,csid=None,border=True):
        """
        Method for retrieving tiles, does not require Authentication and can be called without instantiation.
        Example:
        >>> png = GeoDaWS_DynTM.getTile('testuser:B9C118EB30A9EAE19C93902E9F01EF8A',5,7,12)
        """
        cls = pyGWS.GeoDaWebServiceClient()
        cls._url = HOST+"/dyntm/t"
        req = '?ts=%s&z=%s&x=%s&y=%s'%(tileSetID,zoom,x,y)
        if not border:
            req+='&b=0'
        if clid:
            req+='&cl=%s'%(clid)
        if csid:
            req+='&cs=%s'%(csid)
        print cls._url+req
        result = cls._get(req)
        if result.code == 200:
            return result.read()
        else:
            return result
    def listClassifications(self):
        result = self._get('cl',raiseErrors=False)
        if result.code == 200:
            return simplejson.loads(result.read())['classifications']
        else:
            return None
    def deleteClassification(self,clid):
        result = self._delete('cl/%s'%clid)
        return simplejson.loads(result.read())
    def createClassification(self,tileSetID,classes):
        a = array.array(UNSIGNED_ITEM_TYPES[1])
        a.fromlist(classes)
        a = base64.b64encode(zlib.compress(a.tostring()))
        data = {'dat':a,'tsid':tileSetID,'format':'b64zlib'}
        url = self._post('cl',data,raiseErrors=False)
        if url.code == 200:
            return simplejson.loads(url.read())['ClassificationID']
        else:
            return url
    def createClassification2(self,tileSetID,classes):
        a = ','.join(map(str,classes))
        data = {'dat':a,'tsid':tileSetID,'format':'csv'}
        url = self._post('cl',data,raiseErrors=False)
        if url.code == 200:
            return simplejson.loads(url.read())['ClassificationID']
        else:
            return url
    def getClassification(self,clid):
        result = self._get('cl/%s'%clid)
        if result.code == 200:
            return simplejson.loads(result.read())
        else:
            return result
    def listColorSchemes(self):
        result = self._get('colors',raiseErrors=False)
        if result.code == 200:
            return simplejson.loads(result.read())['colorschemes']
        else:
            return None
    def deleteColorScheme(self,csid):
        result = self._delete('colors/%s'%csid)
        return simplejson.loads(result.read())
    def createColorScheme(self,colors,background_color='#000001',border_color='#000000'):
        """
        colors -- list of strings
                Each color should be in HEX RGB format beginning with a '#'.
                The first color in the list provided is assigned to class 2, the next to class 3 and so on.

                Class 0 and Class 1 are reserved for the background and borders respectivly.
                The Background color should NOT be used anywhere else in the color scheme.
                    Since this color will be made transparent.

        Example:
        colors = ['#ff0000','#00ff00','#0000ff']
        client.createColorScheme(colors)
        """
        data = {'colors':','.join(colors)}
        data['background'] = background_color
        data['borders'] = border_color
        result = self._post('colors',data,raiseErrors=False)
        if result.code == 200:
            return simplejson.loads(result.read())['ColorSchemeID']
        else:
            return result
    def getColorScheme(self,csid):
        result = self._get('colors/%s'%csid).read()
        return simplejson.loads(result)
if __name__ == '__main__':
    import time
    #time.sleep(3)
    #import doctest
    #doctest.testmod()

    ### More testing
    AccessKeyID = 'dtmUser'
    AccessKey = 'key'
    client = GeoDaWS_DynTM(AccessKeyID=AccessKeyID,AccessKey=AccessKey)
    shp = open("/home/ubuntu/geoscore/dynTM_example/data/world.shp",'rb')
    shx = open("/home/ubuntu/geoscore/dynTM_example/data/world.shx",'rb')
    print "posting:"
    resp = client.createTileSet(shp,shx)
    print resp

    #cl = [3, 2, 2, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 2, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 3, 3, 3, 2, 2]
    #print "posting:", client.createClassification('testuser:B9C118EB30A9EAE19C93902E9F01EF8A',cl)
    #colors = ['#00ff00','#0000ff']
    #print "posting:", client.createColorScheme(colors)
