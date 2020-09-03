#!/usr/bin/env python3
from zipfile import ZipFile
from datetime import datetime
from urllib.request import urlretrieve
from os.path import basename, isdir, isfile, join
from os import mkdir, listdir
from subprocess import call

# Point to Susannah's Dropbox folder containing *.nc files.
force_download = False
dummy_files_url = "https://www.dropbox.com/sh/bxsiert5zl1rmpd/AACgS4dVWXSf3j0jUQBVky6aa?dl=1"
dummy_files_zip = "docs/dummy_files.zip"

if not isdir("docs"):
    mkdir("docs")

# Download the directory as a zip, if necessary.
try:
    if force_download or not isfile(dummy_files_zip):
        urlretrieve(dummy_files_url, dummy_files_zip)
except Exception as e:
    raise e
else:
    # Get the name of the folder that we'll extract into.
    dummy_files_dir = dummy_files_zip.replace(".zip","")
    try:
        # Extract all the netCDF files from the zip into docs/
        with ZipFile(dummy_files_zip, "r") as z:
            z.extractall(dummy_files_dir)
    except Exception as e:
        raise e
    else:
        # Get the file listing for the extracted zip.
        files = []
        for f in listdir(dummy_files_dir):
            if f.endswith(".nc"):
                files.append(join(dummy_files_dir, f))

# Loop the list of files and call ncdump.
for f in files:
    print(f"# Calling ncdump utility from shell ...\n {f} \n")
    call(f"ncdump -h '{f}' > {dummy_files_dir}/{basename(f)}.cdl", shell=True)
    #print(f"ncdump -h '{f}' > '{dummy_files_dir}/{basename(f)}.cdl'")
