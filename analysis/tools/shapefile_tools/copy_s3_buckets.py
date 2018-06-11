""" s3 tools
"""
import time
from boto.s3.connection import S3Connection

def copyBucket(srcBucketName, dstBucketName, maxKeys = 100):
  conn = S3Connection(awsAccessKey, awsSecretKey)

  srcBucket = conn.get_bucket(srcBucketName);
  dstBucket = conn.get_bucket(dstBucketName);

  resultMarker = ''
  while True:
    keys = srcBucket.get_all_keys(max_keys = maxKeys, marker = resultMarker)

    for k in keys:
      print 'Copying ' + k.key + ' from ' + srcBucketName + ' to ' + dstBucketName

      t0 = time.clock()
      dstBucket.copy_key(k.key, srcBucketName, k.key)
      print time.clock() - t0, ' seconds'

    if len(keys) < maxKeys:
      print 'Done'
      break

    resultMarker = keys[maxKeys - 1].key

if __name__ == "__main__":
    # copy keys from old buckets to new buckets in the new geoscore account
    awsAccessKey="AKIAIMHVB6IU7X7O55TQ"
    awsSecretKey="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"
    
    copyBucket("geoscore.mapnik","geoscore.software" , maxKeys = 100)

    copyBucket("geoscore.shapefile","geoscore.shapefiles" , maxKeys = 100)
    
    #$s3cmd cp s3://geoscore.mapnik s3://geoscore.software --recursive
    #ERROR: S3 error: 403 (AccessDenied): Access Denied

    # Solution: Temporarily make all source buckets public from AWS console
