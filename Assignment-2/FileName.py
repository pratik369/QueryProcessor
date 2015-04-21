from os import listdir
import re


def getFiles(path):

    print path

    index_list = []
    data_list = []      # insert the path to the directory of interest here

    # Get the names of initial data and index files
    for f in listdir(path):
        if re.search('_index', f):
            index_list.append(f)
        if re.search('_data', f):
            data_list.append(f)

    index_list.sort()
    data_list.sort()

    return index_list, data_list


