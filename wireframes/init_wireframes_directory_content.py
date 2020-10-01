#!/usr/bin/env python3
from zipfile import ZipFile
from datetime import datetime
from urllib.request import urlretrieve
from os.path import basename, isdir, isfile, join
from os import mkdir, listdir
from subprocess import call
from difflib import context_diff #unified_diff

# Point to Susannah's Dropbox folder containing *.nc files.
force_download = False
dummy_files_url = "https://www.dropbox.com/sh/bxsiert5zl1rmpd/AACgS4dVWXSf3j0jUQBVky6aa?dl=1"
dummy_files_zip = "dummy_files.zip"

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
        # Extract all the netCDF files from the zip into local dir.
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

# If for some reason there are NO files, raise an exception:
if len(files)==0:
    raise Exception("ERROR: No local wireframes found! Exit.")

# Make it if there's not already a directory `dummy_files_markup`.
if not isdir("dummy_files_markup"):
    mkdir("dummy_files_markup")

# Get the directory listing for `dummy_files_markup`.
dummy_files_markup = listdir("dummy_files_markup/")

# Loop the list of files and call ncdump.
for f in files:
    print(f"\n# Call ncdump util [ {f} ]")
    call(f"ncdump -h '{f}' > {dummy_files_dir}/{basename(f)}.cdl", shell=True)

    # If marked up copy of this file exists, diff to `dummy_files_diff`:
    if f"{basename(f)}.cdl" in dummy_files_markup:
        marked_up = join("dummy_files_markup/", f"{basename(f)}.cdl")
        print(f" - Diff: {marked_up}\n")

        # Make it if there's not already a directory `dummy_files_diff`.
        if not isdir("dummy_files_diff"):
            mkdir("dummy_files_diff")

        # Read the from and to files for the diff.
        with open(f"{f}.cdl", "r") as ff, open(marked_up, "r") as tf:
            ffile, tfile = ff.readlines(), tf.readlines()

        # Compare `f` to `markup` and write difference to file.
        call(f"diff {f}.cdl dummy_files_markup/{basename(f)}.cdl > dummy_files_diff/{basename(f)}.cdl", shell=True)
        # with open(f"dummy_files_diff/{basename(f)}.cdl", "w") as d:
        #     for ln in context_diff(ffile, tfile):
        #         d.write(str(ln))
        #     d.write("\n")
