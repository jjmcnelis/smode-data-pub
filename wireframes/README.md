# wireframes

This folder stores and version controls content related to S-MODE/PO.DAAC collaboration on dataset wireframes.

**Intended use of this content:**

Whenever Susannah makes substantial changes to the wireframes, I'll run the Python script `init_wireframes_directory_content.py` to:

* download the latest wireframes (netCDF4) to this directory and unzip them, 
* dump CDL representation of each wireframe to a text file with a `.cdl` extension.
* "curated" version of the CDL dumps in adjacent directory [`dummy_files_markup`](dummy_files_markup/)

CDLs in `dummy_files` are diffed with my marked up versions in `dummy_files_markup` automatically every time I run the python script, so they could highlight any discrepancies between my markups and the current outputs of Susannah's MATLAB scripts. See [`dummy_files_diff`](dummy_files_diff/)

**Links:**

Latest *DummyFiles* on Dropbox: https://www.dropbox.com/sh/bxsiert5zl1rmpd/AACgS4dVWXSf3j0jUQBVky6aa?dl=0 

(Replace trailing `0` with `1` to trigger zip+download service on Dropbox side.)


