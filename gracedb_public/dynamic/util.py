# X. Li 2023
# This file contains utility functions for the gracedb_public package

# system/Python-built-in dependencies   
import  os
import  shutil
from    typing  import Union

def re_punctuation() -> str:
    '''
    return the translation method with all punctuations removed
    
    Returns
    -------
    str
        translation method
    '''
    # string.punctuation -> r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    # keep '.' for file extension
    return str.maketrans('', '', r"""!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~""")

def fixdir(path : Union[str, list]) -> None:
    ''' 
    create path if not already

    Parameters
    ----------
    path : str, list
        path to be created

    Returns
    -------
    None
    '''
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

def removedir(path : Union[str, list]) -> None:
    ''' 
    remove dir if not already
    
    Parameters
    ----------
    path : str, list
        path to be removed

    Returns
    -------
    None
    '''
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

def cleardir(path : Union[str, list]) -> None:
    ''' 
    clear dir if not already
    
    Parameters
    ----------
    path : str, list
        path to be cleared

    Returns
    -------
    None
    '''
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

def getSize(path : str) -> float:
    ''' 
    return the size of the file in MB
    
    Parameters
    ----------
    path : str
        path to the file

    Returns
    -------
    size : float
        size of the file in MB
    '''
    size = os.path.getsize(path)
    size = size / 1024 / 1024
    return size

def get_dirSize(path : str) -> float:
    ''' 
    return the size of the directory in MB

    Parameters
    ----------
    path : str
        path to the directory

    Returns
    -------
    total : float
        size of the directory in MB
    '''
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += getSize(fp)    # size in MB
    return total

def getNumberofFiles(path : str) -> int:
    ''' 
    return the number of files in the directory

    Parameters
    ----------
    path : str
        path to the directory

    Returns
    -------
    int
        number of files in the directory
    '''
    return len(os.listdir(path))