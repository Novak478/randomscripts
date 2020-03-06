#This function rechecks the transient folder it is reading from one final time so that it can split any large files into smaller digestible chunks.
oversized_files_list = []
files = dbutils.fs.ls(dbfsInput)

for x in files:
    #measured in bytes..
    #1.0GB check
    if(x.size > 1000000000):
      oversized_files_list.append(x.name)

# Splits files over 1 GB into smaller files. Deletes previous large file.

if (len(oversized_files_list) > 0):
  for filename in oversized_files_list:
    print("Running split for {}...".format(filename))
    newInput = dbfsInput.replace("dbfs:/mnt/", "/dbfs/mnt/") #this is needed for accessing files within mnt point of transient bucket.
    wholepath = newInput + filename
    lines_per_file = 1000000

    smallfile = None
    with open(wholepath, "r+", encoding='latin-1') as bigfile: 
        for lineno, line in enumerate(bigfile):
            if lineno % lines_per_file == 0:
                if smallfile:
                    smallfile.close()
                small_filename = filename.replace('^logfile.log', '^_{}_logfile.log'.format(lineno + lines_per_file)) #renaming file to be separate from old
                newfilename = newInput + small_filename
                smallfile = open(newfilename, "w") #writing new small file
            smallfile.write(line)
        if smallfile:
            smallfile.close()
    removepath = wholepath.replace("/dbfs/", "dbfs:/") #needed to delet old files.
    dbutils.fs.rm(removepath) #removing old large file from mnt point when they have been split
else:
  print("no files to split!")