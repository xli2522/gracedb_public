# X. Li 2023
import string
import os
import shutil

def re_punctuation() -> str:
    '''return the translation method with all punctuations removed'''
    # string.punctuation -> r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    # keep '.' for file extension
    return str.maketrans('', '', r"""!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~""")

def fixdir(path : [str, list]) -> None:
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

def removedir(path : [str, list]) -> None:
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

def cleardir(path : [str, list]) -> None:
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