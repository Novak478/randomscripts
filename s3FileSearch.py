import os
import pandas as pd
import re
import mmap

def s3FileSearch():
    # input the files you are searching for    
    filesWeAreSearchingFor = ['example1.csv','example2.csv']
    fileTypeWeAreSearchingFor = ".csv"
    # Gets list of buckets and write to .csv file
    getBucketNames = 'aws s3api list-buckets --query "Buckets[].Name" > bucketnames.csv'
    # Runs aws cli command -- this will work as long as you have it installed with access keys.
    os.system(getBucketNames)
    bucketDataFrame = pd.read_csv('bucketnames.csv')
    # dropping first and last row where value is "[" and "]"
    bucketDataFrameWithoutFirstAndLastRow = bucketDataFrame[1:-1]
    found = " WAS found in: "
    notFound = " NOT found in: "
    star = "*** "
    for row in bucketDataFrameWithoutFirstAndLastRow.iterrows():
        bucketNameWhole = str(row)
        bucketName = ""
        try:
                bucketName = re.search('    "(.+?)"', bucketNameWhole).group(1)
        except AttributeError:
               print('Invalid bucket name.')
        # Get list of contents per bucket and save in txt file. --dryrun command makes it so that the command is not actually ran. Using cp because it 
        # allows for --exclude and --include args. Rm does too, but it is more risky...
        searchPart = "aws s3 cp s3://"
        searchPart = searchPart + bucketName
        searchPart = searchPart + ' s3://bucket/zackn/ --recursive --exclude "*" --include "*' + fileTypeWeAreSearchingFor + '"--dryrun > '
        searchPart = searchPart + bucketName + "CONTENTS.txt"
        fileHoldingS3Contents = bucketName + "CONTENTS.txt"
        #Files all .csv files in bucket and writes to individual contents file.
        os.system(searchPart)
        #Searching content file for file we are looking for (example1.csv, example2.csv).
        for file in filesWeAreSearchingFor:
                if os.stat(fileHoldingS3Contents).st_size == 0:
                        print(file + notFound + fileHoldingS3Contents)
                else:
                        f = open(fileHoldingS3Contents)
                        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                        if s.find(file) != -1:
                                print(star + file + found + fileHoldingS3Contents + star)

if __name__ == "__s3FileSearch__":
    s3FileSearch()