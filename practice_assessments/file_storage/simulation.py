import json
import math
import string
import re
import random
import sys
import traceback
import functools
from collections import OrderedDict

from datetime import datetime, timedelta

import numpy
import sortedcontainers

files = {}
times = {}
expires = {}
limit = 24000
space = limit * 1024

def get_size(size):
    s = 0
    if size.endswith("kb"):
        asint = size[:-2]
        s = int(asint) * 1024
    return s

def FILE_UPLOAD_AT(timestamp, file_name, file_size, ttl=None):
    upload = FILE_UPLOAD(file_name, file_size)

    # Expiring file?
    if ttl is not None:
        expires[file_name] = ttl

    # Timestamped file?
    if upload.startswith("uploaded"):
        times[file_name] = timestamp
        return f"uploaded at {file_name}"

    return upload

def FILE_UPLOAD(file_name, size):
    global space
    s = get_size(size)
    # Can hold file?
    if(s > space):
        return "File too big"
    
    # Already have file?
    if file_name in files:
        return "Already have"
    
    # Store
    files[file_name] = s
    space -= s
    
    # Good
    return f"uploaded {file_name}"

def FILE_GET(file_name):
    return f"got {file_name}" if file_name in files else "file not found"


def FILE_GET_AT(timestamp, file_name):
    output = FILE_GET(file_name)
    current = datetime.fromisoformat(timestamp)

    # Is this a ttl file?
    if file_name in expires:
        ttl = expires.get(file_name)
        expiry = current + timedelta(seconds=ttl)

        # Expired?
        if(expiry >= current):
            return "file not found"

    # regular file
    return output.replace("got ", "got at ")

def FILE_COPY(source, dest):
    files[dest] = files.get(source) if source in files else None
    return f"copied {source} to {dest}"

def FILE_COPY_AT(timestamp, file_from, file_to):
    FILE_COPY(file_from, file_to)
    times[file_to] = timestamp
    return f"copied at {file_from} to {file_to}"

def FILE_SEARCH(prefix):
    # Find files matching name
    matches = list(filter(lambda x: x.startswith(prefix), files.keys()))

    # Sort by size
    matches.sort(key=lambda x: files.get(x), reverse=True)

    return f"found {matches}".replace("'", "")

def FILE_SEARCH_AT(timestamp, prefix):
    output = FILE_SEARCH(prefix)
    return output.replace("found ", "found at ")

def ROLLBACK(timestamp):

    # Delete anything after the rollback
    rollback = datetime.fromisoformat(timestamp)

    deletions = []
    for file,size in files.items():
        if file in times:
            filetime = datetime.fromisoformat(times.get(file))
            if filetime > rollback:
                #print("too new, rollbak")
                deletions.append(file)


    for file in deletions:
        if file in expires:
            expires.pop(file)
        if file in times:
            times.pop(file)
        if file in files:
            files.pop(file)

    return f"rollback to {timestamp}"

def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    output = []
    for event in list_of_lists:
        op = event[0]
        if "FILE_GET" == op:
            output.append(FILE_GET(event[1]))
        elif "FILE_GET_AT" == op:
            output.append(FILE_GET_AT(event[1], event[2]))
        elif "FILE_UPLOAD" == op:
            output.append(FILE_UPLOAD(event[1], event[2]))
        elif "FILE_UPLOAD_AT" == op:
            ttl = None
            if len(event) > 4:
                ttl = event[4]
            output.append(FILE_UPLOAD_AT(event[1], event[2], event[3], ttl))
        elif "FILE_COPY" == op:
            output.append(FILE_COPY(event[1], event[2]))
        elif "FILE_COPY_AT" == op:
            output.append(FILE_COPY_AT(event[1], event[2], event[3]))
        elif "FILE_SEARCH" == op:
            output.append(FILE_SEARCH(event[1]))
        elif "FILE_SEARCH_AT" == op:
            output.append(FILE_SEARCH_AT(event[1], event[2]))
        elif "ROLLBACK" == op:
            output.append(ROLLBACK(event[1]))
        else:
            raise NotImplementedError(f"Don't know how to {op}")

    return output
    #return ["uploaded Cars.txt", "got Cars.txt", "copied Cars.txt to Cars2.txt", "got Cars2.txt"]
    #pass
