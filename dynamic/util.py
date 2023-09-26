# X. Li 2023
import numpy as np
import string
import os
import shutil

def re_punctuation():
    '''return the translation method with all punctuations removed'''
    return str.maketrans('', '', string.punctuation)

def fixdir(path):
    ''' create path if not already
    path: tuple or list'''
    if isinstance(path, str):
        if not os.path.exists(path):
            os.makedirs(path)
    elif isinstance(path, (list, tuple)):
        for i in path:
            if not os.path.exists(i):
                os.makedirs(i)
    else: 
        raise TypeError('Only str, list, and tuple are allowed')
    return

def removedir(path):
    ''' remove dir if not already
    path: tuple or list'''
    if isinstance(path, str):
        if os.path.exists(path):
            shutil.rmtree(path)
    elif isinstance(path, (list, tuple)):
        for i in path:
            if os.path.exists(i):
                shutil.rmtree(i)
    else: 
        raise TypeError('Only str, list, and tuple are allowed')
    return

def cleardir(path):
    ''' clear dir if not already
    path: tuple or list'''
    if isinstance(path, str):
        if os.path.exists(path):
            for f in os.listdir(path):
                os.remove(os.path.join(path, f))
    elif isinstance(path, (list, tuple)):
        for i in path:
            if os.path.exists(i):
                for f in os.listdir(path):
                    os.remove(os.path.join(path, f))
    else: 
        raise TypeError('Only str, list, and tuple are allowed')
    return