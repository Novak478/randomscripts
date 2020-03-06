import io
from io import BytesIO
import gzip
from gzip import GzipFile
import boto3
now = dbutils.widgets.get("dateHourUTCToRun")
# now = "2020020507"
dbutils.fs.refreshMounts()
dc = dbutils.widgets.get("dc")
# dc = "ex"
dbfsInput  = "dbfs:/mnt/s3bucket/logs/{dc}/{now}/".format(dc=dc, now=now)

#Checks for gzipped files.
gzip_file_check = dbutils.fs.ls(dbfsInput)
still_gzipped_files = []

for x in gzip_file_check:
  if(".gz" in x.name):
    still_gzipped_files.append(x.name)

#If there is a gzipped file in the transient bucket, this function unzips it and deletes the previously zipped file.

if (len(still_gzipped_files) > 0):
  print("Number of files still gzipped: {}".format(len(still_gzipped_files)))
  splits = dbfsInput.split('/')
  source_bucket = splits[2] #source_bucket for boto3
  keywithoutfile = '/'.join(splits[3:-1]) + "/" #key without filename for boto3
  for file in still_gzipped_files:
    wholepath = dbfsInput + file #creating direct file path for dbfs rm.
    try: 
      s3 = boto3.client('s3') 
      old_key = keywithoutfile + file
      oldfile = s3.get_object(Bucket=source_bucket, Key=old_key)['Body'].read() #getting s3 object and reading 
      newfile = gzip.GzipFile(None,'rb',fileobj=BytesIO(oldfile)) #unzipping file

      new_filename = file.replace(".gz", "")
      new_key = keywithoutfile + new_filename
      print("Running file: {}".format(new_key))
      s3.upload_fileobj(Fileobj=newfile,Bucket=source_bucket,Key=new_key) #uploading unzipped contents of old file to new file.
      print("Deleting {}...".format(wholepath))
      dbutils.fs.rm(wholepath) #after unzipping into new file, we want the old unzipped one to be deleted.
    except:
      print("There was an error trying to unzip the file! Moving {} to dead letter queue.".format(file))
      dbutils.fs.mv(wholepath, "/dbfs/mnt/bucket2/logs/dlq/")
else:
  print("no files are gzipped in {}.".format(dbfsInput))