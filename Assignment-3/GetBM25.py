__author__ = 'Vivek & Pratik'

from math import log

k1 = 1.2
b = 0.75


def getBM25(n, f, qf, dl, avdl):
    # n - total number of documents in collection
    # f - number of documents that contain term t
    # qf - frequency of term t in doc d
    # dl - length of document
    # avdl - average length of documents in collection

    K = compute_K(dl, avdl)
    first = log((n - f + 0.5)/(f + 0.5))
    second = ((k1 + 1) * qf) / (K + qf)
    return first * second


def compute_K(dl, avdl):
    return k1 * ((1-b) + (b * (float(dl)/float(avdl))))
