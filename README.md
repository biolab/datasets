# Orange data set repository

A collection of descriptions of data sets that are served in Data Set widget in [Orange](http://orange.biolab.si).

Each data set is described with a record that contains the following attributes:

    info = {
        "description": "",  # description of the data set
        "name": "", # data set file name
        "title": "",  # a short title (less then 40 characters)
        "tags": [],  # any tags
        "target": "categorical",  # categorical, numeric, None
        "version": "1.0",  # data set version
        "year": None,  # year the original data set was published
        "collection": "",  # name of original repository (like UCI)
        "instances": 178,  # number of data instances
        "missing": False,  # contains missing values?
        "variables": 14,  # number of independent variables
        "source": "https://archive.ics.uci.edu/ml/datasets/Wine",  # web page of original
        "size": 10991,  # data size in bytes
        "file": "http://butler.fri.uni-lj.si/datasets/wine.tab",  # the file will be downloaded from
    }
