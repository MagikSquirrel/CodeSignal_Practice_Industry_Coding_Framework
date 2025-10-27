import json
import math
import string
import re
import random
import sys
import traceback
import functools
from collections import OrderedDict

import numpy
import sortedcontainers

files = {}
limit = 24000
space = limit * 1024

def get_size(size):
    s = 0
    if size.endswith("kb"):
        asint = size[:-2]
        s = int(asint) * 1024
    return s

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
    return f"got {file_name}" if file_name in files else "NOT FOUND"

def FILE_COPY(source, dest):
    files[dest] = files.get(source) if source in files else None
    return f"copied {source} to {dest}"

def FILE_SEARCH(prefix):
    # Find files matching name
    matches = list(filter(lambda x: x.startswith(prefix), files.keys()))

    # Sort by size
    matches.sort(key=lambda x: files.get(x), reverse=True)

    # TODO Limit 10
    return f"found {matches}".replace("'", "")

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
        elif "FILE_UPLOAD" == op:
            output.append(FILE_UPLOAD(event[1], event[2]))
        elif "FILE_COPY" == op:
            output.append(FILE_COPY(event[1], event[2]))
        elif "FILE_SEARCH":
            output.append(FILE_SEARCH(event[1]))
        else:
            raise NotImplemented

    return output
    #return ["uploaded Cars.txt", "got Cars.txt", "copied Cars.txt to Cars2.txt", "got Cars2.txt"]
    #pass
